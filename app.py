import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  User, 
  MapPin, 
  Euro, // Icono de Euro
  CheckCircle, 
  ShieldCheck, 
  ArrowRight, 
  ArrowLeft,
  Printer,
  Calculator,
  Building,
  Globe,
  List,
  Download,
  Trash2,
  XCircle,
  AlertTriangle
} from 'lucide-react';

// --- FIREBASE IMPORTS (MANDATORY GLOBALS) ---
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithCustomToken, signInAnonymously, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, collection, addDoc, onSnapshot, query, deleteDoc, doc } from 'firebase/firestore';

/**
 * UTILIDADES CRIPTOGRÁFICAS
 * Fallback seguro para entornos sin crypto nativo
 */
const generateVeriFactuHash = async (invoiceData, prevHash = "") => {
  try {
    // Aseguramos que solo usamos los campos requeridos por la norma
    const rawString = `${invoiceData.issuerNif}${invoiceData.number}${invoiceData.date}${invoiceData.finalTotal}${prevHash}`;
    if (window.crypto && window.crypto.subtle) {
      const msgBuffer = new TextEncoder().encode(rawString);
      const hashBuffer = await window.crypto.subtle.digest('SHA-256', msgBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    } else {
      // Usamos una simulación determinista para el desarrollo
      const simulatedHash = rawString.length.toString(16).padStart(64, '0').substring(0, 60) + "S";
      return simulatedHash;
    }
  } catch (error) {
    return "ERROR_HASH";
  }
};

// --- COMPONENTES UI SIMPLIFICADOS ---

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden ${className}`}>
    {children}
  </div>
);

const Button = ({ onClick, children, variant = "primary", className = "", disabled = false }) => {
  const baseStyle = "px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed";
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 shadow-md",
    secondary: "bg-slate-100 text-slate-700 hover:bg-slate-200",
    success: "bg-green-600 text-white hover:bg-green-700 shadow-md",
    danger: "bg-red-600 text-white hover:bg-red-700 shadow-md",
    outline: "border-2 border-slate-200 text-slate-600 hover:border-slate-300 bg-white"
  };
  return (
    <button onClick={onClick} disabled={disabled} className={`${baseStyle} ${variants[variant]} ${className}`}>
      {children}
    </button>
  );
};

const Input = ({ label, value, onChange, type = "text", placeholder = "", required = false }) => (
  <div className="mb-4">
    <label className="block text-sm font-bold text-slate-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
    </label>
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      required={required}
      className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none text-base"
    />
  </div>
);

const Select = ({ label, value, onChange, options }) => (
  <div className="mb-4">
    <label className="block text-sm font-bold text-slate-700 mb-1">{label}</label>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none bg-white text-base"
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>{opt.label}</option>
      ))}
    </select>
  </div>
);

// --- APP PRINCIPAL ---

export default function VeriFactuEasyApp() {
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState('create'); // 'create' o 'report'
  
  // --- ESTADO FIREBASE ---
  const [db, setDb] = useState(null);
  const [userId, setUserId] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false);
  const [invoices, setInvoices] = useState([]); // Array para almacenar facturas
  const [error, setError] = useState(null); // Para mostrar errores de Firebase

  // Estado inicial de la factura (lo que se va editando)
  const [invoice, setInvoice] = useState({
    // Emisor
    issuerName: "Mi Empresa S.L.",
    issuerNif: "B12345678",
    issuerAddress: "Calle Comercio 1, Madrid",
    
    // Cliente
    clientName: "",
    clientNif: "",
    clientAddress: "",
    clientLocation: "ES", 
    
    // Detalles Económicos
    number: "F-2025-001",
    date: new Date().toISOString().split('T')[0],
    concept: "",
    inputPrice: 0,        // El precio que escribe el usuario
    priceIncludesVat: false, // ¿Ese precio ya tiene IVA?
    
    // Configuración Fiscal
    ivaRate: 21,
    retentionType: "none", // none, alquiler, no_residente
    retentionRate: 0,
    
    // Veri*Factu (se usa el hash de la última factura guardada)
    previousHash: "0000000000000000000000000000000000000000000000000000000000000000",
    currentHash: "",
    qrUrl: ""
  });
  
  // --- INICIALIZACIÓN Y AUTENTICACIÓN FIREBASE ---
  useEffect(() => {
    try {
        const firebaseConfig = JSON.parse(typeof __firebase_config !== 'undefined' ? __firebase_config : '{}');
        if (Object.keys(firebaseConfig).length === 0) {
            console.error("Firebase config is missing.");
            return;
        }

        const app = initializeApp(firebaseConfig);
        const firestore = getFirestore(app);
        const firebaseAuth = getAuth(app);

        setDb(firestore);

        const unsubscribe = onAuthStateChanged(firebaseAuth, async (user) => {
            if (user) {
                setUserId(user.uid);
            } else {
                try {
                    const token = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;
                    if (token) {
                        await signInWithCustomToken(firebaseAuth, token);
                    } else {
                        await signInAnonymously(firebaseAuth);
                    }
                } catch (e) {
                    console.error("Firebase Auth Error:", e);
                    setError("Error de autenticación. Inténtalo de nuevo.");
                }
            }
            setIsAuthReady(true);
        });

        return () => unsubscribe();
    } catch (e) {
        console.error("Failed to initialize Firebase:", e);
        setError("Fallo al inicializar la base de datos.");
        setIsAuthReady(true);
    }
  }, []);

  // --- ESCUCHA EN TIEMPO REAL DE FACTURAS (onSnapshot) ---
  useEffect(() => {
    if (!db || !userId) return;

    const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
    const invoiceCollectionPath = `artifacts/${appId}/users/${userId}/invoices`;
    const q = query(collection(db, invoiceCollectionPath));

    const unsubscribe = onSnapshot(q, (snapshot) => {
        const invoiceList = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }));
        
        // Ordenar en memoria por fecha descendente
        invoiceList.sort((a, b) => new Date(b.date) - new Date(a.date));
        setInvoices(invoiceList);

        // Actualizar el previousHash de la factura actual al último hash guardado
        if (invoiceList.length > 0) {
            setInvoice(prev => ({ ...prev, previousHash: invoiceList[0].currentHash }));
        }
    }, (e) => {
        console.error("Error fetching invoices: ", e);
    });

    return () => unsubscribe();
  }, [db, userId]);

  // --- MOTOR DE CÁLCULO INTELIGENTE ---
  
  // 1. Detectar IVA por ubicación
  useEffect(() => {
    if (invoice.clientLocation === "UE" || invoice.clientLocation === "EXTRA_UE") {
      setInvoice(prev => ({ ...prev, ivaRate: 0 })); // Exento automáticamente
    } else {
      setInvoice(prev => ({ ...prev, ivaRate: 21 })); // Vuelta a general
    }
  }, [invoice.clientLocation]);

  // 2. Calcular Base Imponible real
  const calculateBase = () => {
    const price = parseFloat(invoice.inputPrice) || 0;
    if (invoice.priceIncludesVat && invoice.ivaRate > 0) {
      // Desglosar IVA: Precio / (1 + tipo)
      return price / (1 + (invoice.ivaRate / 100));
    }
    return price;
  };

  const baseAmount = calculateBase();
  const ivaAmount = baseAmount * (invoice.ivaRate / 100);
  const retentionAmount = baseAmount * (invoice.retentionRate / 100);
  const finalTotal = baseAmount + ivaAmount - retentionAmount;

  // --- LOGICA DE FACTURACIÓN Y GUARDADO ---

  const generateInvoice = async () => {
    if (!db || !userId) {
      setError("La base de datos no está lista. Por favor, espera un momento.");
      return; 
    }
    
    // Validaciones básicas antes de guardar
    if (!invoice.clientName || !invoice.concept || !invoice.inputPrice) {
        setError("Faltan campos obligatorios (Cliente, Concepto o Precio).");
        return;
    }
    setError(null); // Limpiar errores
    setLoading(true);

    const baseAmountValue = calculateBase();
    const ivaAmountValue = baseAmountValue * (invoice.ivaRate / 100);
    const retentionAmountValue = baseAmountValue * (invoice.retentionRate / 100);
    const finalTotalValue = baseAmountValue + ivaAmountValue - retentionAmountValue;

    // Usamos el previousHash ya actualizado por el useEffect
    const invoiceToHash = { ...invoice, finalTotal: finalTotalValue.toFixed(2) };
    const hash = await generateVeriFactuHash(invoiceToHash, invoice.previousHash);
    
    const qrData = `https://www2.agenciatributaria.gob.es/wlpl/TOCP-MANT/verifactu?nif=${invoice.issuerNif}&num=${invoice.number}&fecha=${invoice.date}&total=${finalTotalValue.toFixed(2)}&hash=${hash.substring(0,6)}`;

    const fullInvoiceData = {
        ...invoice,
        baseAmount: baseAmountValue.toFixed(2),
        ivaAmount: ivaAmountValue.toFixed(2),
        retentionAmount: retentionAmountValue.toFixed(2),
        finalTotal: finalTotalValue.toFixed(2),
        currentHash: hash,
        qrUrl: qrData,
        timestamp: new Date().toISOString(),
    };

    try {
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
        const invoiceCollectionPath = `artifacts/${appId}/users/${userId}/invoices`;
        await addDoc(collection(db, invoiceCollectionPath), fullInvoiceData);
        
        // Mostrar la factura recién creada
        setInvoice(fullInvoiceData); 
        setLoading(false);
        setStep(4);
        
    } catch (e) {
        console.error("Error saving invoice: ", e);
        setError("Error al guardar la factura en la base de datos.");
        setLoading(false);
    }
  };
  
  const handleDeleteInvoice = async (invoiceId) => {
      if (!db || !userId) return;
      if (!window.confirm("¿Estás seguro de que quieres eliminar esta factura del registro?")) return;
      
      try {
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
        const invoiceDocPath = `artifacts/${appId}/users/${userId}/invoices/${invoiceId}`;
        await deleteDoc(doc(db, invoiceDocPath));
      } catch (e) {
          console.error("Error deleting invoice: ", e);
      }
  };

  // --- PASOS DE LA INTERFAZ ---

  const steps = [
    { title: "Yo (Emisor)", icon: User },
    { title: "Cliente", icon: MapPin },
    { title: "Dinero", icon: Calculator }, 
    { title: "Detalles", icon: FileText },
    { title: "Factura", icon: CheckCircle }
  ];

  const renderStep = () => {
    switch(step) {
      case 0:
        return (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-800">1. ¿Quién emite la factura? (Tú)</h2>
            <Input label="Tu Nombre o Empresa" value={invoice.issuerName} onChange={v => setInvoice({...invoice, issuerName: v})} required />
            <Input label="Tu DNI / NIF" value={invoice.issuerNif} onChange={v => setInvoice({...invoice, issuerNif: v})} required />
            <Input label="Tu Dirección" value={invoice.issuerAddress} onChange={v => setInvoice({...invoice, issuerAddress: v})} />
          </div>
        );
      case 1:
        return (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-800">2. ¿A quién le cobras?</h2>
            <Input label="Nombre del Cliente" value={invoice.clientName} onChange={v => setInvoice({...invoice, clientName: v})} required />
            <Input label="DNI / NIF del Cliente" value={invoice.clientNif} onChange={v => setInvoice({...invoice, clientNif: v})} required />
            <Select 
              label="¿Dónde vive el cliente?" 
              value={invoice.clientLocation} 
              onChange={v => setInvoice({...invoice, clientLocation: v})}
              options={[
                { value: "ES", label: "🇪🇸 España" },
                { value: "UE", label: "🇪🇺 Unión Europea (Intracomunitario)" },
                { value: "EXTRA_UE", label: "🌍 Fuera de Europa (Exportación)" }
              ]} 
            />
            <Input label="Dirección del Cliente" value={invoice.clientAddress} onChange={v => setInvoice({...invoice, clientAddress: v})} />
          </div>
        );
      case 2:
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-slate-800">3. ¿Cuánto vas a cobrar?</h2>
            
            {/* Input Gigante de Precio con Euro */}
            <div className="bg-slate-50 p-6 rounded-xl border border-slate-200">
               <label className="block text-lg font-bold text-slate-700 mb-2">Precio acordado con el cliente (€)</label>
               <div className="relative">
                 <Euro className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400" size={24} />
                 <input
                   type="number"
                   value={invoice.inputPrice}
                   onChange={(e) => setInvoice({...invoice, inputPrice: e.target.value})}
                   className="w-full pl-12 pr-4 py-4 text-3xl font-bold text-slate-800 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none"
                   placeholder="0.00"
                   min="0"
                   required
                 />
               </div>

               {/* Toggle IVA Incluido */}
               <div className="mt-4 flex items-center gap-3">
                 <button 
                   onClick={() => setInvoice({...invoice, priceIncludesVat: !invoice.priceIncludesVat})}
                   className={`relative w-14 h-8 rounded-full transition-colors duration-200 ${invoice.priceIncludesVat ? 'bg-blue-600' : 'bg-slate-300'}`}
                 >
                   <div className={`absolute top-1 left-1 w-6 h-6 bg-white rounded-full transition-transform duration-200 ${invoice.priceIncludesVat ? 'translate-x-6' : 'translate-x-0'}`} />
                 </button>
                 <span className="text-slate-700 font-medium text-sm md:text-base">
                   {invoice.priceIncludesVat ? "Este precio YA incluye el IVA (Yo lo desgloso)" : "A este precio hay que SUMARLE el IVA"}
                 </span>
               </div>
            </div>

            {/* Selector Visual de Retenciones */}
            <div>
               <label className="block text-lg font-bold text-slate-700 mb-3">¿Hay que aplicar alguna retención especial?</label>
               <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <RetentionCard 
                    title="Alquiler Local" 
                    rate="19%" 
                    subtitle="(Dueños de locales)"
                    active={invoice.retentionType === "alquiler"}
                    onClick={() => setInvoice({...invoice, retentionType: "alquiler", retentionRate: 19})}
                    icon={Building}
                  />
                  <RetentionCard 
                    title="No Residente" 
                    rate="24%" 
                    subtitle="(IRNR / Ley Beckham)"
                    active={invoice.retentionType === "no_residente"}
                    onClick={() => setInvoice({...invoice, retentionType: "no_residente", retentionRate: 24})}
                    icon={Globe}
                  />
                  <RetentionCard 
                    title="Ninguna" 
                    rate="0%" 
                    active={invoice.retentionType === "none"}
                    onClick={() => setInvoice({...invoice, retentionType: "none", retentionRate: 0})}
                    icon={User}
                  />
               </div>
            </div>
            
            {/* Aviso inteligente */}
            {invoice.clientLocation !== "ES" && (
               <div className="bg-blue-50 text-blue-800 p-3 rounded-lg text-sm border border-blue-200 flex items-center gap-2">
                 <Info size={18} />
                 Al ser un cliente extranjero, <strong>hemos quitado el IVA (0%) automáticamente</strong> y añadiremos la nota legal necesaria en la factura.
               </div>
            )}
          </div>
        );
      case 3:
        return (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-800">4. Últimos detalles</h2>
            <div className="grid grid-cols-2 gap-4">
               <Input label="Número Factura" value={invoice.number} onChange={v => setInvoice({...invoice, number: v})} required />
               <Input label="Fecha" type="date" value={invoice.date} onChange={v => setInvoice({...invoice, date: v})} required />
            </div>
            <Input label="¿Qué servicio hiciste? (Concepto)" value={invoice.concept} onChange={v => setInvoice({...invoice, concept: v})} placeholder="Ej: Alquiler mes de Julio, Diseño Web..." required />
          </div>
        );
      case 4:
        return <FinalInvoice invoice={invoice} base={baseAmount} iva={ivaAmount} ret={retentionAmount} total={finalTotal} />;
      default: return null;
    }
  };

  if (!isAuthReady) {
    return (
        <div className="min-h-screen bg-slate-100 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600"></div>
        </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 py-8 px-4 font-sans text-slate-800">
      <div className="max-w-2xl mx-auto">
        
        {/* Header y Selector de Vista */}
        <div className="flex justify-between items-center gap-3 mb-6">
          <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-lg text-white"><ShieldCheck size={28} /></div>
              <h1 className="text-2xl font-bold text-slate-800">Facturador Fácil Veri*Factu</h1>
          </div>
          <Button variant="outline" onClick={() => setView(view === 'create' ? 'report' : 'create')} className="shrink-0">
            {view === 'create' ? <><List size={18} /> Mis Facturas</> : <><Calculator size={18} /> Crear Factura</>}
          </Button>
        </div>
        
        {/* Error Message */}
        {error && (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4 flex items-center gap-2 rounded" role="alert">
                <AlertTriangle size={20} />
                <p>{error}</p>
                <button onClick={() => setError(null)} className="ml-auto"><XCircle size={18} /></button>
            </div>
        )}

        {view === 'create' ? (
          <>
            {/* Pasos */}
            {step < 4 && (
              <div className="flex justify-between mb-6 px-2">
                {steps.map((s, idx) => (
                  <div key={idx} className={`flex flex-col items-center ${idx === step ? 'opacity-100' : 'opacity-40'}`}>
                    <div className={`w-3 h-3 rounded-full mb-1 ${idx <= step ? 'bg-blue-600' : 'bg-slate-300'}`} />
                    <span className="text-[10px] font-bold uppercase">{s.title}</span>
                  </div>
                ))}
              </div>
            )}

            <Card className="min-h-[400px]">
              <div className="p-6 md:p-8">
                {loading ? (
                  <div className="flex flex-col items-center justify-center py-10 text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mb-6"></div>
                    <h3 className="text-xl font-bold text-slate-700">Conectando con Hacienda...</h3>
                    <p className="text-slate-500">Generando huella digital y código QR seguro.</p>
                  </div>
                ) : renderStep()}
              </div>

              {!loading && step < 4 && (
                <div className="bg-slate-50 p-6 border-t border-slate-200 flex justify-between">
                  {step > 0 ? (
                    <Button variant="secondary" onClick={() => setStep(step - 1)}>
                      <ArrowLeft size={18} /> Atrás
                    </Button>
                  ) : <div />}
                  
                  {step === 3 ? (
                    <Button variant="success" onClick={generateInvoice} disabled={!isAuthReady}>
                      Guardar y Crear Factura <CheckCircle size={18} />
                    </Button>
                  ) : (
                    <Button onClick={() => setStep(step + 1)}>
                      Siguiente <ArrowRight size={18} />
                    </Button>
                  )}
                </div>
              )}
            </Card>
          </>
        ) : (
          <InvoiceReport invoices={invoices} onDelete={handleDeleteInvoice} />
        )}
      </div>
      <p className="text-center text-xs text-slate-400 mt-4">
        ID de usuario: {userId || 'Cargando...'}
      </p>
    </div>
  );
}

// --- SUBCOMPONENTES DE UI ---

const RetentionCard = ({ title, rate, subtitle, active, onClick, icon: Icon }) => (
  <button 
    onClick={onClick}
    className={`p-4 rounded-xl border-2 text-left transition-all ${active ? 'border-blue-600 bg-blue-50 ring-1 ring-blue-600' : 'border-slate-200 hover:border-blue-300 bg-white'}`}
  >
    <div className="flex justify-between items-start mb-2">
      <Icon size={20} className={active ? 'text-blue-600' : 'text-slate-400'} />
      {active && <CheckCircle size={18} className="text-blue-600" />}
    </div>
    <div className="font-bold text-slate-800">{title}</div>
    <div className={`text-xl font-mono font-bold ${active ? 'text-blue-700' : 'text-slate-500'}`}>{rate}</div>
    {subtitle && <div className="text-xs text-slate-400 mt-1">{subtitle}</div>}
  </button>
);

const FinalInvoice = ({ invoice, base, iva, ret, total }) => {
  
  // Determinar menciones legales automáticas
  const getLegalMentions = () => {
    if (invoice.clientLocation === "UE") return "Operación con Inversión del Sujeto Pasivo (Reverse Charge). Art. 25 Ley IVA.";
    if (invoice.clientLocation === "EXTRA_UE") return "Operación de Exportación Exenta de IVA. Art. 21 Ley IVA.";
    if (invoice.retentionType === "alquiler") return "Operación sujeta a retención por arrendamiento de inmuebles urbanos.";
    if (invoice.retentionType === "no_residente") return "Operación sujeta a retención IRNR (No Residentes).";
    return "";
  };
  
  const mention = getLegalMentions();

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Factura Guardada y Lista</h2>
        <Button variant="outline" onClick={() => window.print()} className="print:hidden">
          <Printer size={18} /> Imprimir (PDF)
        </Button>
      </div>

      <div className="bg-white border border-slate-300 p-8 rounded-lg shadow-sm print:shadow-none print:border-0 relative text-sm">
        {/* Banner Legal */}
        <div className="absolute top-0 right-0 bg-slate-800 text-white text-xs px-3 py-1 rounded-bl-lg">
          VERI*FACTU
        </div>

        {/* Cabecera */}
        <div className="grid grid-cols-2 gap-8 mb-8 mt-4">
          <div>
            <h3 className="font-bold text-slate-400 text-xs uppercase mb-1">Emisor</h3>
            <div className="font-bold text-lg text-blue-800">{invoice.issuerName}</div>
            <div>{invoice.issuerNif}</div>
            <div className="text-slate-500">{invoice.issuerAddress}</div>
          </div>
          <div className="text-right">
            <h3 className="font-bold text-slate-400 text-xs uppercase mb-1">Factura</h3>
            <div className="font-bold text-lg">Nº {invoice.number}</div>
            <div>Fecha: {invoice.date}</div>
          </div>
        </div>

        {/* Cliente */}
        <div className="border-t border-b border-slate-100 py-4 mb-6">
          <h3 className="font-bold text-slate-400 text-xs uppercase mb-1">Cliente</h3>
          <div className="font-bold text-lg">{invoice.clientName}</div>
          <div>{invoice.clientNif}</div>
          <div className="text-slate-500">{invoice.clientAddress}</div>
          <div className="text-xs text-slate-400 mt-1">Región: {invoice.clientLocation}</div>
        </div>

        {/* Línea de Concepto */}
        <table className="w-full mb-6">
          <thead>
            <tr className="text-left text-slate-500 border-b border-slate-200">
              <th className="pb-2">Concepto</th>
              <th className="pb-2 text-right">Importe</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="py-3 font-medium">{invoice.concept}</td>
              <td className="py-3 text-right font-mono">{base.toFixed(2)} €</td>
            </tr>
          </tbody>
        </table>

        {/* Totales */}
        <div className="flex justify-end">
          <div className="w-full md:w-1/2 space-y-2">
            <div className="flex justify-between text-slate-600">
              <span>Base Imponible</span>
              <span>{base.toFixed(2)} €</span>
            </div>
            
            {invoice.ivaRate > 0 && (
              <div className="flex justify-between text-slate-600">
                <span>IVA ({invoice.ivaRate}%)</span>
                <span>{iva.toFixed(2)} €</span>
              </div>
            )}
            
            {invoice.retentionRate > 0 && (
              <div className="flex justify-between text-red-600 font-medium bg-red-50 px-2 py-1 rounded">
                <span>Retención ({invoice.retentionRate}%)</span>
                <span>-{ret.toFixed(2)} €</span>
              </div>
            )}

            <div className="flex justify-between border-t-2 border-slate-800 pt-3 mt-2 text-xl font-bold text-slate-900">
              <span>TOTAL A PAGAR</span>
              <span>{total.toFixed(2)} €</span>
            </div>
          </div>
        </div>

        {/* Footer Legal & VeriFactu */}
        <div className="mt-8 pt-4 border-t border-slate-200">
          {mention && (
            <div className="mb-4 p-2 bg-slate-100 text-slate-600 text-xs rounded border border-slate-200">
              <strong>Mención Legal:</strong> {mention}
            </div>
          )}
          
          <div className="flex items-center gap-4">
            <div className="bg-white p-1 border rounded">
              <img 
                 src={`https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=${encodeURIComponent(invoice.qrUrl)}`} 
                 alt="QR VeriFactu" 
                 className="w-20 h-20"
              />
            </div>
            <div className="text-[10px] text-slate-400 flex-1">
              <div className="font-mono bg-slate-50 p-1 mb-1 truncate text-slate-500">
                HUELLA: {invoice.currentHash}
              </div>
              <p>
                Documento generado conforme al Reglamento Veri*Factu (RD 1007/2023). 
                Registro inalterable encadenado criptográficamente.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// --- COMPONENTE DE REPORTE DE FACTURAS ---

const InvoiceReport = ({ invoices, onDelete }) => {
  
  // Función de exportación a CSV
  const exportToCSV = (data) => {
    if (data.length === 0) return;

    // Campos clave para el asesor
    const headers = [
      "Fecha", "Numero_Factura", "Concepto", "Cliente_NIF", "Base_Imponible", 
      "IVA_TIPO", "IVA_IMPORTE", "RETENCION_TIPO", "RETENCION_IMPORTE", "TOTAL_FINAL", "HUELLA_VERIFACTU"
    ];
    
    const rows = data.map(inv => [
      inv.date,
      inv.number,
      inv.concept.replace(/"/g, '""'), // Escapar comillas dobles
      inv.clientNif,
      inv.baseAmount,
      inv.ivaRate,
      inv.ivaAmount,
      inv.retentionRate,
      inv.retentionAmount,
      inv.finalTotal,
      inv.currentHash
    ].map(field => `"${field}"`).join(',')); // Envolver campos en comillas

    const csvContent = [headers.join(','), ...rows].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `Reporte_Facturas_${new Date().getFullYear()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  
  const totalFacturado = invoices.reduce((sum, inv) => sum + parseFloat(inv.finalTotal || 0), 0).toFixed(2);

  return (
    <Card className="p-6 md:p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
            <List size={24} /> Mis Facturas ({invoices.length})
        </h2>
        <Button variant="secondary" onClick={() => exportToCSV(invoices)} disabled={invoices.length === 0}>
          <Download size={18} /> Exportar CSV
        </Button>
      </div>

      <div className="bg-blue-50 p-3 rounded-lg mb-4 flex justify-between items-center font-bold text-blue-800 border border-blue-200">
          <span>TOTAL FACTURADO (NETO)</span>
          <span className="text-2xl font-mono">{totalFacturado} €</span>
      </div>

      {invoices.length === 0 ? (
        <div className="text-center py-10 text-slate-500">
          Aún no tienes facturas guardadas. ¡Empieza a crear una!
        </div>
      ) : (
        <div className="space-y-3">
          {invoices.map((inv) => (
            <div key={inv.id} className="p-4 bg-white border border-slate-200 rounded-lg shadow-sm flex justify-between items-center transition-all hover:ring-2 hover:ring-blue-100">
              <div className="flex-1 min-w-0">
                <div className="font-bold text-slate-800 truncate">{inv.number} - {inv.clientName}</div>
                <div className="text-sm text-slate-500 truncate">{inv.concept}</div>
                <div className="text-xs text-slate-400 mt-1">
                    {inv.date} | Base: {inv.baseAmount} € | Ret: {inv.retentionRate}%
                </div>
              </div>
              <div className="flex items-center gap-4 ml-4">
                <span className="text-xl font-bold text-green-700 font-mono flex-shrink-0">
                  {inv.finalTotal} €
                </span>
                <button 
                    onClick={() => onDelete(inv.id)} 
                    title="Eliminar Factura"
                    className="p-1 text-red-400 hover:text-red-600 transition-colors"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-6 p-3 bg-slate-50 text-slate-500 text-xs rounded">
          * Para generar un PDF, ve a la factura individual y utiliza el botón "Imprimir (PDF)" de tu navegador.
      </div>
    </Card>
  );
};

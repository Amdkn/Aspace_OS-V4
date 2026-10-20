// ═══════════════════════════════════════════════════════════════════════════
// MASTER PROFILE — noyau de données canonique et souverain (SSOT)
// OMK Office / JaaS 1.0 — Topologie tri-polaire (Pôles 1 · 3 · 2)
// Découplage Zero Trust : Artefact Public (Verified Candidate Passport)
//                        vs Vault Privé (Secure Intake Vault)
// ═══════════════════════════════════════════════════════════════════════════
// Remplace dossier.schema.ts comme contrat canonique. Le dossier d'intake
// reste la forme de collecte ; le Master Profile est la forme projetée.

export type WorkAuthorizationStatus =
  | 'EAD_C08'
  | 'EAD_C09'
  | 'EAD_TPS'
  | 'GREEN_CARD'
  | 'US_CITIZEN'
  | 'I797C_RECEIPT'; // renouvellement en cours, récépissé I-797C

export type RegionalCorridor =
  | 'CVG_HEBRON'
  | 'NORTHERN_KY_ERLANGER_FLORENCE'
  | 'GREATER_CINCINNATI_NORTH';

export type DispatchQueue =
  | 'AMAZON_AIR_CVG'
  | 'DHL_ERLANGER'
  | 'KROGER_BLUE_ASH'
  | 'WAYFAIR_FLORENCE';

export type SkillCode =
  | 'FORKLIFT_OSHA'
  | 'OSHA_10'
  | 'BILINGUAL_EN_FR'
  | 'WMS_RF_SCAN'
  | 'DRIVER_LICENSE';

export interface SkillItem {
  code: SkillCode;
  name: string;
  hourlyValue: number;        // plus-value horaire directe, ex. 2.50
  verifiedByOffice: boolean;
  certificateRef?: string;
}

export interface WorkHistoryEntry {
  company: string;
  role: string;
  startDate: string;          // ISO YYYY-MM
  endDate?: string;           // ISO YYYY-MM | 'present'
  highlights: string[];
  duties?: string;
  location?: { country?: string; city?: string; state?: string };
  reasonForLeaving?: string;
}

export interface EducationEntry {
  institution: string;
  degree: string;
  fieldOfStudy?: string;
  graduationYear?: number;
}

// ── Artefact Public : Verified Candidate Passport ───────────────────────────
// Distribuable aux recruteurs / ATS sans exposer de données critiques.
export interface PublicPassport {
  omkId: string;              // ex. "OMK-2026-CVG-2192"
  fullName: string;
  preferredName?: string;
  email: string;
  phone: string;
  workStatus: WorkAuthorizationStatus;
  workStatusCertifiedByOffice: boolean;
  targetCorridor: RegionalCorridor;
  skillsPassport: SkillItem[];
  negotiatedWageMin: number;  // ex. 23.50
  negotiatedWageMax: number;  // ex. 27.50
  dispatchQueues: DispatchQueue[];
  atsResumeRef?: string;      // chemin DOCX/PDF généré
  workHistory: WorkHistoryEntry[];
  education: EducationEntry[];
  qrVerificationRef?: string; // QR employeur
}

// ── Artefact Privé : Secure Intake Vault ────────────────────────────────────
// Stockage local ou Supabase chiffré uniquement. Projeté dans les champs
// d'onboarding formels sous contrôle direct de l'opérateur.
export interface PrivateVault {
  ssn: string;                // jamais dans l'artefact public
  dateOfBirth: string;        // ISO YYYY-MM-DD
  address: {
    street: string;
    street2?: string;
    city: string;
    state: string;
    zip: string;
    country: string;
  };
  emergencyContact: { fullName: string; relationship: string; phone: string };
  directDeposit: {
    bankName: string;
    routingNumber: string;    // 9 digits
    accountNumber: string;
    accountType: 'CHECKING' | 'SAVINGS' | 'PAYCARD';
    bankCountry: 'USA' | 'Canada';
  };
  tax: {
    filingStatus: 'single' | 'married' | 'head_of_household';
    w4Allowances: number;
    electronicW2Consent: boolean;
  };
  referralCode?: string;      // Acte 3.5-5 : 50 $/filleul, 6 = 300 $ amortis
}

// ── PORTE DE SIGNATURE — acte juridique, jamais automatisée ────────────────
export interface SignatureGate {
  signatureAuthorized: boolean;   // autorisation explicite du client
  authorizedAt?: string;          // ISO timestamp
  scope: string[];                // titres exacts des documents couverts
  signatureStyle: 'TYPE' | 'CANVAS';
  legalTextsReviewed: boolean;    // le client a relu les textes
}

// ── Master Profile (SSOT) ──────────────────────────────────────────────────
export type MasterProfileStatus = 'DRAFT' | 'VERIFIED' | 'DISPATCHED' | 'PLACED';

export interface MasterProfile {
  // Métadonnées système
  omkId: string;
  profileKind: 'DEMO' | 'REAL';   // ex. DEMO = "Abdoulaye Traoré", REAL = "Sallou Camara"
  createdAt: string;
  updatedAt: string;
  status: MasterProfileStatus;

  // Pôle 1 — Légal & Conformité (Acte 1.1-1)
  legal: {
    workStatus: WorkAuthorizationStatus;
    workAuthNumber?: string;
    workAuthExpiration?: string;   // ISO date
    receiptNoticeNumber?: string;  // I-797C si renouvellement en cours
    alienRegistrationNumber?: string;
    ataCertifiedTranslations: boolean;
    notarizedAffidavits: boolean;
  };

  // Pôle 3 — Carrière & Moteur JaaS 1.0 (Actes 3.1 & 3.2)
  career: PublicPassport;

  // Pôle 2 — Vault Privé, Zero Trust (chiffrement local)
  vault: PrivateVault;

  // Porte de signature — contrôle humain déterministe
  signatureGate: SignatureGate;
}

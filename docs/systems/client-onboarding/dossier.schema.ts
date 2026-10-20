// Client Onboarding Dossier — single source of truth, mapped to any portal.
// One dossier per client. Never ask twice for the same datum.

export interface PostalAddress {
  street: string;
  city: string;
  state: string;
  zip: string;
}

export interface Person {
  firstName: string;          // legal first name, as on ID
  middleName?: string;
  lastName: string;           // legal last name, as on ID
  preferredName?: string;
  email: string;
  phone: string;
  dateOfBirth: string;       // ISO YYYY-MM-DD
}

export interface Banking {
  accountType: "checking" | "savings";
  accountNumber: string;
  bankName: string;
  bankCountry?: "USA" | "Canada";
  routingNumber: string;      // 9 digits
}

export interface TaxInfo {
  filingStatus: "single" | "married" | "head_of_household";
  ssn: string;               // full SSN — handle with Vault-level care
  w4ExtraWithholding?: number;
}

export interface JobEntry {
  employer: string;
  title: string;
  duties?: string;
  location?: { country?: string; city?: string; state?: string };
  startDate: string;         // ISO YYYY-MM
  endDate?: string;          // ISO YYYY-MM | "present"
  reasonForLeaving?: string;
}

export interface EducationEntry {
  school: string;
  degree: string;
  fieldOfStudy?: string;
  graduationYear?: number;
}

export interface EmergencyContact {
  fullName: string;
  relationship: string;
  phone: string;
}

export interface ClientDossier {
  client: Person;
  address: PostalAddress;
  identity: {
    ssn: string;
  };
  banking: Banking;                 // Direct Deposit
  tax: TaxInfo;                     // W-2 Consent, W-4
  workHistory: JobEntry[];          // Work History
  education: EducationEntry[];      // Education
  emergencyContact: EmergencyContact;
  // Portal-specific credentials live in the Secure Vault, never here.
  authorizations: {
    signatureAuthorized: boolean;   // PORTE DE SIGNATURE — client explicit OK
    authorizedAt?: string;          // ISO timestamp of the client's approval
    scope: string[];                // task titles covered by the authorization
  };
}

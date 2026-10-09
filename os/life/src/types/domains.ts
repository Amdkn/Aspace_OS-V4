/** Domain types — canonical merge of the 8 ld01…ld08 stores (Phase 1 reduction).
 *  The zustand ld*.store.ts files were removed; only the ParaItem type survives,
 *  imported by para components and hooks. Single source of truth. */
export interface ParaItem {
  id: string;
  title: string;
  description: string;
  content?: string; // V0.6.1 Narrative / Tactic content
  status: 'active' | 'completed' | 'on-hold' | 'paused' | 'archived';
  updatedAt: number;
  createdAt: number; // V0.6.1 Timestamp
  // --- NOUVEAU (V0.4.1) ---
  pillars?: string[];
  resources?: string[];
  progress?: number;
  domain?: string; // Using string to avoid circular dependency, will map to LifeWheelDomain
  archivedAt?: number;
}

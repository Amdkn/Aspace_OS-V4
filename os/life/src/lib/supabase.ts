// src/lib/supabase.ts
// D13-01 — FAIL-FAST explicite à la frontière de confiance.
// Fini le client silencieux vers le vide : sans VITE_SUPABASE_URL /
// VITE_SUPABASE_ANON_KEY, le boot lève une erreur explicite, sauf en mode
// local-only opt-in (VITE_LIFE_LOCAL_ONLY=true) où la persistance est
// explicitement locale et le shell affiche une bannière visible.
import { createClient } from '@supabase/supabase-js';

function readEnv(name: string): string | undefined {
  try {
    if (typeof import.meta !== 'undefined' && (import.meta as any).env?.[name]) {
      return (import.meta as any).env[name] as string;
    }
  } catch { /* noop */ }
  if (typeof process !== 'undefined' && process.env?.[name]) {
    return process.env[name];
  }
  return undefined;
}

/** Mode dégradé opt-in explicite : persistance locale uniquement, démarrage sans compte. */
export const LIFE_LOCAL_ONLY = readEnv('VITE_LIFE_LOCAL_ONLY') === 'true';

const supabaseUrl = readEnv('VITE_SUPABASE_URL');
const supabaseAnonKey = readEnv('VITE_SUPABASE_ANON_KEY');

if ((!supabaseUrl || !supabaseAnonKey) && !LIFE_LOCAL_ONLY) {
  throw new Error(
    '[Life OS] Supabase non configuré : définissez VITE_SUPABASE_URL et ' +
    'VITE_SUPABASE_ANON_KEY, ou démarrez en mode local explicite avec VITE_LIFE_LOCAL_ONLY=true.'
  );
}

export const supabase = createClient(
  // En mode local-only, URL inerte : refus de connexion immédiat, jamais de
  // persistance fantôme. Le shell ne l'appelle pas dans ce mode (bypass App.tsx).
  supabaseUrl ?? 'http://127.0.0.1:0',
  supabaseAnonKey ?? 'local-only',
  {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: false,
    }
  }
);

export async function getUser() {
  try {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
  } catch {
    return null;
  }
}

export async function getCurrentUserId(): Promise<string | null> {
  const user = await getUser();
  return user?.id ?? null;
}

export async function getSession() {
  const { data: { session } } = await supabase.auth.getSession();
  return session;
}

export async function signOut() {
  await supabase.auth.signOut();
}

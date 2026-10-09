/**
 * MuseWebAdapter — SurfaceDriver pour muse.ai
 *
 * Pattern repris de miuuyy/codex-chatgpt-web : la surface web est pilotée
 * en navigateur persisté et exposée comme un modèle au harness.
 * Ici : surface = muse.ai (A0), harness = Claude Code via /v1/messages.
 *
 * Les sélecteurs CSS sont centralisés dans SELECTORS.md et chargés ici.
 * Règle : si un sélecteur ne matche plus, on échoue EXPLICITEMENT
 * (jamais de bascule silencieuse).
 */
import { chromium, type BrowserContext, type Page } from "playwright";
import { readFileSync } from "node:fs";

export interface Selectors {
  input: string;
  sendButton: string;
  /** Présent quand le composer est prêt (fini de générer). */
  sendAction: string;
  /** Présent pendant la génération. */
  stopAction: string;
  threadContainer: string;
  /** `[message-body="true"]` — l'adapter prend le dernier (.last()). */
  streamingMessage: string;
  newChatButton: string;
}

export interface TurnEvidence {
  threadUrl: string;
  fullText: string;
}

const BRIDGE_CHAT_NAME = "Claude Code Bridge";

export class MuseWebAdapter {
  private ctx: BrowserContext | null = null;
  private page: Page | null = null;
  private sel: Selectors;

  constructor(
    private profileDir: string,
    selectorsJsonPath: string,
  ) {
    this.sel = JSON.parse(readFileSync(selectorsJsonPath, "utf-8"));
  }

  /** Ouvre le navigateur persisté et vérifie la session muse.ai. */
  async connect(): Promise<void> {
    this.ctx = await chromium.launchPersistentContext(this.profileDir, {
      headless: false, // le login initial se fait à la main, une fois
    });
    this.page = this.ctx.pages()[0] ?? (await this.ctx.newPage());
    await this.page.goto("https://muse.ai/", { waitUntil: "domcontentloaded" });
    // Échoue explicitement si pas de session (l'utilisateur logge à la main).
    const input = this.page.locator(this.sel.input);
    await input.waitFor({ timeout: 15_000 }).catch(() => {
      throw new Error(
        "[muse_web] pas de session muse.ai détectée : connecte-toi une fois " +
          "dans le navigateur du bridge, puis relance.",
      );
    });
  }

  /** Trouve ou crée le side chat dédié à la session Claude Code. */
  async ensureBridgeChat(): Promise<string> {
    const page = this.requirePage();
    // 1. Chercher un chat existant par son nom accessible (role=button, nom=titre).
    const existing = page.getByRole("button", { name: BRIDGE_CHAT_NAME });
    if ((await existing.count()) > 0) {
      await existing.first().click();
      await page.waitForURL(/thread/, { timeout: 10_000 });
      return page.url();
    }
    // 2. Sinon le créer.
    await page.locator(this.sel.newChatButton).click();
    // Nommer le chat si l'UI le permet (best effort, non bloquant).
    await page.waitForURL(/thread/, { timeout: 10_000 });
    return page.url();
  }

  /**
   * Envoie un prompt et streame la réponse token par token (diff de texte).
   * onToken reçoit les deltas ; résout avec la preuve du tour.
   */
  async send(
    prompt: string,
    onToken: (delta: string) => void,
  ): Promise<TurnEvidence> {
    const page = this.requirePage();
    const threadUrl = await this.ensureBridgeChat();

    const input = page.locator(this.sel.input);
    await input.click();
    await input.fill(prompt);
    await page.locator(this.sel.sendButton).click();

    // Streaming : on poll le message assistant et on émet les deltas.
    const msg = page.locator(this.sel.streamingMessage).last();
    await msg.waitFor({ timeout: 30_000 }).catch(() => {
      throw new Error("[muse_web] aucune réponse assistant détectée après envoi.");
    });

    let seen = "";
    for (;;) {
      const text = (await msg.innerText().catch(() => "")) ?? "";
      if (text.length > seen.length) {
        onToken(text.slice(seen.length));
        seen = text;
      }
      // Fin de génération : le slot d'action rebascule de "stop" vers "send".
      // (signal binaire, bien plus fiable que la disparition d'un bouton)
      const done = (await page.locator(this.sel.sendAction).count()) > 0;
      if (done) {
        // Dernière lecture pour ne rien perdre.
        const final = (await msg.innerText().catch(() => seen)) ?? seen;
        if (final.length > seen.length) onToken(final.slice(seen.length));
        return { threadUrl, fullText: final };
      }
      await page.waitForTimeout(250);
    }
  }

  async close(): Promise<void> {
    await this.ctx?.close();
    this.ctx = null;
    this.page = null;
  }

  private requirePage(): Page {
    if (!this.page) throw new Error("[muse_web] adapter non connecté (connect() d'abord).");
    return this.page;
  }
}

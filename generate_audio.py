import asyncio
import os
import edge_tts

VOICE = "de-DE-KatjaNeural"
RATE = "-15%"
PITCH = "+5Hz"

audio_targets = {
    # System & Modul-Ankündigungen
    "modul_anlaute": "Anlaute hören",
    "modul_silben": "Silben schwingen",
    "modul_zehnerfeld": "Zehnerfeld bis 10",
    "modul_1x1": "Ein mal Ein Blitzrechnen",
    "modul_zehnermulti": "Zehner Multiplikation",
    "modul_halbschriftlich_mul": "Halbschriftlich multiplizieren",
    "modul_wortarten": "Wortarten bestimmen",
    "modul_rechtschreibung": "Rechtschreibung üben",
    "feedback_falsch": "Versuche es noch einmal!",

    # Wortschatz 30 Silben-Wörter (Klasse 1)
    "silbe_hund": "Hund", "silbe_baer": "Bär", "silbe_fisch": "Fisch", "silbe_maus": "Maus", 
    "silbe_baum": "Baum", "silbe_haus": "Haus", "silbe_katze": "Katze", "silbe_sonne": "Sonne", 
    "silbe_blume": "Blume", "silbe_affe": "Affe", "silbe_ente": "Ente", "silbe_apfel": "Apfel", 
    "silbe_vogel": "Vogel", "silbe_auto": "Auto", "silbe_schule": "Schule", "silbe_aepfel": "Äpfel", 
    "silbe_schiff": "Schiff", "silbe_wolke": "Wolke", "silbe_tomate": "Tomate", "silbe_elefant": "Elefant", 
    "silbe_banane": "Banane", "silbe_kamel": "Kamel", "silbe_rakete": "Rakete", "silbe_giraffe": "Giraffe", 
    "silbe_aubergine": "Aubergine", "silbe_pinguin": "Pinguin", "silbe_anemone": "Anemone", 
    "silbe_marienkaefer": "Marienkäfer", "silbe_schmetterling": "Schmetterling", "silbe_schildkroete": "Schildkröte",

    # Wortarten-Begriffe (Klasse 3)
    "wort_haus": "Haus", "wort_baum": "Baum", "wort_kind": "Kind", "wort_schule": "Schule",
    "wort_katze": "Katze", "wort_hund": "Hund", "wort_blume": "Blume", "wort_sonne": "Sonne",
    "wort_laufen": "laufen", "wort_springen": "springen", "wort_singen": "singen", "wort_tanzen": "tanzen",
    "wort_schnell": "schnell", "wort_laut": "laut", "wort_schoen": "schön", "wort_klein": "klein",

    # Rechtschreib-Begriffe (Klasse 3)
    "rs_hund": "Hund", "rs_hand": "Hand", "rs_wald": "Wald", "rs_brod": "Brot", 
    "rs_berg": "Berg", "rs_zug": "Zug", "rs_sieb": "Sieb", "rs_korb": "Korb"
}

os.makedirs("audio", exist_ok=True)

async def generate_all():
    print(f"Starte Prüfung und Generierung aller Audio-Assets ({len(audio_targets)} Ziele)...\n")
    generated, skipped = 0, 0

    for filename, text in audio_targets.items():
        output_path = f"audio/{filename}.mp3"
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            skipped += 1
            continue

        print(f"Erstelle: {filename}.mp3 -> '{text}'...")
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(output_path)
        generated += 1

    print(f"\nFertig! {generated} neue Audio-Dateien erzeugt, {skipped} beibehalten.")

if __name__ == "__main__":
    asyncio.run(generate_all())

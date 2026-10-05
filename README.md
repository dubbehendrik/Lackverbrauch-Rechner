# Lackverbrauch-Rechner

Interaktive Streamlit-Lehrapp für die grobe Abschätzung von Lackverbrauch, Lackverlusten und Kosten. Gestaltung und Hochschullogo orientieren sich an [temperaturprofil_forward](https://github.com/dubbehendrik/temperaturprofil_forward).

**Live-App:** [lackverbrauch-rechner.streamlit.app](https://lackverbrauch-rechner.streamlit.app/)

## Streamlit Community Cloud

- **Python-Version: 3.11** (unter „Advanced settings“ auswählen)
- Repository: `dubbehendrik/Lackverbrauch-Rechner`
- Branch: `main`
- Main file path: `streamlit_lackverbrauch_app.py`
- Abhängigkeiten werden aus `requirements.txt` installiert; keine Secrets notwendig.

Ein GitHub-Repository allein ist noch keine laufende App. In [Streamlit Community Cloud](https://share.streamlit.io/) „Create app“ wählen, diese Angaben setzen und „Deploy“ anklicken.

## Lokal starten

Python 3.11 empfohlen; Python 3.12 ebenfalls unterstützt.

```bash
pip install -r requirements.txt
streamlit run streamlit_lackverbrauch_app.py
```

## Bedienung

1. Beschichtete Fläche pro Bauteil, mittlere Trockenschichtdicke und Lackeigenschaften eingeben. Jede Eingabe nennt ihre Einheit.
2. Rechenweg wählen: bekannte Festkörperdichte, Dichteschätzung aus TDS oder direkter Volumenweg.
3. Taktzeit [min/Stück], Stück/h oder Zielstückzahl für einen Zeitraum vorgeben. Die Pause zwischen den Spritzvorgängen [s] ist Bestandteil des Takts.
4. Schichtmodell festlegen: Schichten/Tag, Schichtdauer, verfügbare Produktionsstunden/Schicht, Tage/Woche, Produktionswochen/Jahr.
5. Vorschau aktualisiert sich nach Enter bzw. Verlassen des Feldes. „Szenario übernehmen“ speichert den Stand unveränderlich. Mit „Szenario behalten“ werden Szenarien ergänzt, andernfalls ersetzt.
6. Diagramm und Zeitraum wählen, Referenzszenario für absolute/prozentuale Abweichungen auswählen. Reset setzt die Eingaben zurück und löscht die gespeicherten Szenarien.

Szenarien werden nur in der aktuellen Sitzung gespeichert. Für dauerhafte Ergebnisse Export verwenden.

## Modell

Bekannte Festkörperdichte:

`m_LK,Stück = A · h̄ · ρ_FK / (ε_FK · MNG)`

`ṁ_LK = m_LK,Stück / t`

TDS-Dichteschätzung:

`ρ_FK ≈ ρ_LK · ε_FK / φ_FK`

Direkter Volumenweg:

`V_LK,Stück = A · h̄ / (φ_FK · MNG)`

Diese Beziehungen sind Größengleichungen mit konsistenten Einheiten und dimensionslosen Anteilen. Eingaben in µm, Gew.-%, Vol.-%, kg/L und Minuten werden intern umgerechnet. LK bezeichnet flüssigen Lack, FK die trockene Festkörperschicht.

Alle TDS-Angaben müssen denselben Produktzustand betreffen. ε_FK ist der Festkörpermassenanteil, φ_FK der Festkörpervolumenanteil. Die geschätzte Dichte bleibt sichtbar. Dichteschätzung und direkter Volumenweg ergeben bei gleichen TDS-Werten identische Verbrauchswerte; Schätzgüte kann nur gegen eine unabhängig bekannte Festkörperdichte verglichen werden. Bei Wertebereichen einen bewusst gewählten Einzelwert verwenden.

`t_Spritz = t_Takt − t_Pause`

Ein Werkstück pro Takt; während der Spritzzeit gleichmäßige Lackapplikation. Spritzstrom und Taktmittel werden getrennt ausgewiesen. Die verfügbare Produktionszeit enthält Werkstückpausen; Schichtpausen und Stillstände werden davon abgezogen. Keine doppelte Berücksichtigung der Werkstückpause.

Tag = Schichten × verfügbare Stunden; Woche = Tag × Arbeitstage; Jahr = Woche × Produktionswochen; durchschnittlicher Monat = Jahr / 12. Keine exakte Kalender-/Feiertagsrechnung. Kumulierte Diagramme verwenden verfügbare Produktionsstunden; der Verlauf ist über die Takte gemittelt. Rechnerische Stückzahlen sind kontinuierliche Planungswerte, zusätzlich wird die Anzahl vollständiger Stücke abgerundet. Die Mengenrechnung basiert auf den kontinuierlichen Werten. Bei Zielplanung ist das Ziel für den gewählten Zeitraum exakt enthalten.

`V_Verlust = V_Verbrauch · (1 − MNG)`

`K_Lack = V_Verbrauch · Literpreis`

`K_Verlust = V_Verlust · Literpreis`

Verlust ist äquivalentes Flüssiglackvolumen, das nicht zur vorgesehenen Beschichtung beiträgt. Bestimmungsgemäße Lösemittelverdunstung ist kein MNG-Verlust. Verlustkosten sind Bestandteil der Gesamtkosten. Ein einheitlicher verarbeitungsfertiger Lack, keine Mehrschichtsysteme, Verdünnungs-/Mischungsrechnung, Reserveaufschläge oder Entsorgungskosten. Literpreis bezieht sich auf denselben verarbeitungsfertigen Lack wie Dichte und Festkörperwerte. Alle Kosten folgen der vom Nutzer gewählten Preisbasis (z. B. netto).

## Export

Nur gespeicherte Szenarien, keine ungespeicherte Vorschau:

- CSV: Ergebnisse für alle Zeiträume, Semikolon, Dezimalkomma, UTF-8 mit BOM.
- Excel: Zeitraum-Ergebnisse, vollständige Parameter inklusive Rechenweg, kumulierte Verläufe und Einheiten.
- PNG/SVG: gewählte Diagrammart und Zeitraum, Matplotlib ohne Browser-/Kaleido-Abhängigkeit. Interaktiver Zoom wird nicht exportiert.

## Prüfungen

```bash
python -m unittest discover -s tests -v
```

Referenz-Materialbilanz, Einheitentransformation, Rechenweg-Identität, Takt/Pause, Zielplanung, Jahres-/Monatsrelation, Grenzwerte, Szenario-Schnappschüsse, Reset und Exporte. GitHub Actions prüft Python 3.11 und 3.12.

## Verwendung

Demonstrations- und Lehrzwecke. Eine kommerzielle Verwendung ist nicht gestattet. Hochschullogo aus der bestehenden App unverändert übernommen. Kontakt: Prof. Dr.-Ing. Hendrik Dubbe, hendrik.dubbe@hs-esslingen.de.

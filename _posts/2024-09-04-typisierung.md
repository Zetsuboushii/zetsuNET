---
layout: post
title: "Statische Typisierung :) Schwache Typisierung >:("
date: 2024-09-04
category: Hacken
---

Ich muss einmal meine Gedanken zu Typisierung niederschreiben.

<img src="https://qph.cf2.quoracdn.net/main-qimg-41585198bc6b9576738e54b02b008860-lq" style="max-width: 400px;">

Ich bin ein großer Fan von statischer Typisierung. Aber; was ist statische Typisierung, bzw. schwache Typisierung
überhaupt?

**Statische Typisierung** überprüft Datentypen bereits zur Compile Time, was frühzeitig Fehler verhindert. Bei
**schwacher Typisierung** werden Typen dynamisch zur Laufzeit umgewandelt, was zu unerwartetem Verhalten und schwerer
auffindbaren Fehlen führen kann.

Da wir nun ein besseres Verständnis zu der Unterscheidung haben, hier ein paar Vorteile von statischer Typisierung:

1. Fehlererkennung zur Kompilierzeit: In statisch typisierten Sprachen werden viele Fehler (z. B. falsche Datentypen,
   Typinkonsistenzen) bereits während der Kompilierung erkannt, was die Wahrscheinlichkeit von Laufzeitfehlern
   reduziert. Das erhöht die Zuverlässigkeit und Sicherheit des Codes.

2. Bessere Lesbarkeit und Wartbarkeit: Da der Datentyp einer Variablen explizit im Code definiert ist, wird die Absicht
   des Programmierers klarer. Das erleichtert anderen Entwicklern (oder dem Entwickler selbst zu einem späteren
   Zeitpunkt) das Verständnis und die Wartung des Codes.

3. Leistungsoptimierung: Statisch typisierte Sprachen ermöglichen es dem Compiler, spezifische Optimierungen
   vorzunehmen,
   da er genau weiß, welche Datentypen verwendet werden. Dies kann zu einer besseren Performance führen, insbesondere in
   rechenintensiven oder speicherkritischen Anwendungen.

4. Erhöhte Robustheit bei großen Projekten: In großen Projekten, die von mehreren Entwicklern bearbeitet werden,
   minimiert
   statische Typisierung das Risiko, dass durch versehentliche Typänderungen Fehler eingeführt werden. Änderungen im
   Code brechen nicht still und heimlich die Typensicherheit, was das Risiko von Bugs reduziert.

5. Explizite Konvertierung: Da Type Casting (z. B. von einem int zu einem string) in statisch typisierten Sprachen
   explizit durchgeführt werden müssen, führt dies zu einer klareren und sichereren Codebasis. Implizite
   Konvertierungen,
   die oft zu unerwarteten Ergebnissen führen, werden so vermieden.

Und weil es so spaßig ist, nochmal ein paar Nachteile der schwachen Typisierung:

1. Unvorhersehbares Verhalten zur Laufzeit: In schwach typisierten Sprachen können Typkonvertierungen automatisch und
   implizit durchgeführt werden, was zu unerwarteten Ergebnissen führt. Zum Beispiel können Operationen wie das Addieren
   einer Zahl zu einem String zu inkonsistenten Ergebnissen führen, was die Fehlersuche erschwert. Dabei heraus kommt
   dann so funny Stuff wie in JavaScript:

   ```
   "5" + 2  // ergibt "52"
   "5" - 2  // ergibt 3
   ```

   Es gibt sehr viele lustige Begebenheiten in JavaScript, die diese Sprache für mich unbenutzbar machen. Zum Glück gibt
   es TypeScript; das macht JS deutlich erträglicher.

2. Fehler treten erst zur Laufzeit auf: Schwach typisierte Sprachen erkennen viele Fehler (wie falsche Typen) erst zur
   Laufzeit, was bedeutet, dass solche Fehler in der Entwicklung leicht übersehen werden und erst beim Einsatz der
   Software kritisch werden. In sicherheitsrelevanten oder produktiven Anwendungen kann das schwerwiegende Konsequenzen
   haben.

3. Schwierige Fehlersuche: Da schwach typisierte Sprachen automatisch Typkonvertierungen vornehmen, können Fehler schwer
   zu identifizieren und zu beheben sein. Die Logik eines Codes kann plötzlich durch eine unerwartete Typänderung
   brechen, ohne dass der Entwickler eine klare Warnung erhält.

4. Mangelnde Vorhersehbarkeit: Automatische Typkonvertierungen machen es schwierig, das Verhalten eines Programms zu
   prognostizieren, besonders wenn komplexe Datentypen oder Operationen involviert sind. Dies führt zu einer schwerer zu
   wartenden und unsicheren Codebasis.

Aus diesen Gründen bin ich eher ein Freund von Sprachen wie C oder Java. Python ist wohl mein persönlicher Erzfeind,
teils auch begründet durch die schwache Typisierung, aber das ist eine andere Geschichte. 
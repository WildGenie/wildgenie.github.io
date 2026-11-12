#!/usr/bin/env python3
"""One-off: let links/ show several featured cards and put the Space Apps film above the podcast."""
import json, pathlib
K = pathlib.Path(__file__).resolve().parent.parent / "links"
h = K / "index.html"
s = h.read_text()
eski = s[s.index("      const f = d.featured;"):s.index("      const ul = $(\"links\");")]
yeni = '''      // featured may be one card or a list; extra cards are copies of the first, in order
      const kart = $("featured");
      const liste = [].concat(d.featured || []);
      if (!liste.length) kart.remove();
      liste.forEach((f, i) => {
        const k = i ? kart.parentNode.insertBefore(kart.cloneNode(true), $("links")) : kart;
        if (i) k.querySelectorAll("[id]").forEach((n) => n.removeAttribute("id")), k.removeAttribute("id");
        k.href = f.url;
        if (f.image) k.querySelector("img").src = f.image;
        k.querySelector(".label").textContent = f.label || "";
        k.querySelector("h2").textContent = f.title || "";
        k.querySelector("p").textContent = f.text || "";
        k.querySelector(".cta").textContent = f.cta || "İzle";
      });

'''
assert "f-img" in eski and eski.count("\n") < 20
h.write_text(s.replace(eski, yeni))
j = K / "links.json"
d = json.loads(j.read_text())
podcast = d["featured"] if isinstance(d["featured"], dict) else d["featured"][-1]
d["featured"] = [{
    "label": "NASA Space Apps 2026",
    "title": "Hackathon İki Günde Nasıl Geçer? 14 Görev, Jüri ve Teslim",
    "text": "Bu hafta sonu yarışacak takımlar için 10 dakikalık Türkçe rehber film.",
    "url": "https://youtu.be/WMJfTMu1x5Q",
    "image": "https://i.ytimg.com/vi/WMJfTMu1x5Q/hqdefault.jpg",
    "cta": "Filmi izle"}, podcast]
yeniler = [
    {"title": "Space Apps 2026 Türkçe Rehber", "subtitle": "nasaspaceapps.zeki.website", "url": "https://nasaspaceapps.zeki.website", "icon": "globe"},
    {"title": "14 görev 6 dakikada", "subtitle": "Space Apps 2026 görevleri", "url": "https://youtu.be/6_z98Xyz6xU", "icon": "youtube"}]
d["links"] = yeniler + [l for l in d["links"] if l["url"] not in {y["url"] for y in yeniler}]
j.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("tamam", len(d["featured"]), "öne çıkan,", len(d["links"]), "bağlantı")

"""Export exact figures from Agent_World_NeurIPS_2026.pdf.
Requires macOS Swift/PDFKit and Python Pillow. No network needed.
"""
from pathlib import Path
import subprocess, tempfile
from PIL import Image
root = Path(__file__).resolve().parents[1]
paper = root.parent / 'Agent_World_NeurIPS_2026.pdf'
# Figure bounds measured on a 918 × 1188 rendering; retain figure artwork only.
figures = {
 'intro': (2, (163,104,754,283)),
 'method': (4, (165,110,754,338)),
 'modality_route': (5, (437,745,752,883)),
 'token_num': (2, (483,467,753,602)),
 'qualitative': (9, (164,110,754,465)),
 'agent_num': (9, (164,939,754,1065)),
}
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    swift = '''import Foundation
import PDFKit
import AppKit
let d=PDFDocument(url:URL(fileURLWithPath:CommandLine.arguments[1]))!
for n in [2,4,5,9] {
let p=d.page(at:n-1)!
let img=p.thumbnail(of:NSSize(width:2754,height:3564),for:.mediaBox)
let rep=NSBitmapImageRep(data:img.tiffRepresentation!)!
try! rep.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:CommandLine.arguments[2]+"/page-\\(n).png"))
}
'''
    script = tmp / 'render.swift'
    script.write_text(swift)
    subprocess.run(['swift', '-module-cache-path', str(tmp/'cache'), str(script), str(paper), str(tmp)],check=True)
    for name,(page,box) in figures.items():
        im = Image.open(tmp/f'page-{page}.png').convert('RGB')
        sx,sy=im.width/918,im.height/1188
        im=im.crop(tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate(box)))
        im.save(root/f'static/images/{name}.webp', quality=95, method=6)
        print(name, im.size)

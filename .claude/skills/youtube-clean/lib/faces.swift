import Foundation
import Vision
import AppKit
for p in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: p), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print(p, "noimg"); continue }
  let req = VNDetectFaceRectanglesRequest()
  let h = VNImageRequestHandler(cgImage: cg, options: [:])
  try? h.perform([req])
  let W = Double(cg.width), H = Double(cg.height)
  var out = [String]()
  for f in (req.results ?? []) { let b = f.boundingBox; out.append(String(format: "%.1f,%.1f,%.1f,%.1f", b.minX*W, (1-b.maxY)*H, b.width*W, b.height*H)) }
  print((p as NSString).lastPathComponent, out.joined(separator: " "))
}

import Foundation

let src = "/Users/t.anh/Downloads/BÁO CÁO THỰC TẬP NHÓM 10/BAOCAOTHUCTAPNHOM10.html"
let dest = "/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main/BAOCAOTHUCTAPNHOM10.html"

// Remove existing dest if it exists
try? FileManager.default.removeItem(atPath: dest)

do {
    try FileManager.default.copyItem(atPath: src, toPath: dest)
    print("Success! Copied HTML file to workspace.")
} catch {
    print("Error: \(error)")
}

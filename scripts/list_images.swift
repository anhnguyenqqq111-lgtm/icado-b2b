import Foundation

let htmlPath = "/Users/t.anh/Downloads/BÁO CÁO THỰC TẬP NHÓM 10/BAOCAOTHUCTAPNHOM10.html"
let outputPath = "/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main/tmp/images_list.txt"

do {
    let content = try String(contentsOfFile: htmlPath, encoding: .utf8)
    
    // Regex to match img tags
    let pattern = "<img[^>]+>"
    let regex = try NSRegularExpression(pattern: pattern, options: .caseInsensitive)
    let nsString = content as NSString
    let results = regex.matches(in: content, options: [], range: NSRange(location: 0, length: nsString.length))
    
    var outputText = ""
    outputText += "Total <img> elements found: \(results.count)\n\n"
    
    for (idx, result) in results.enumerated() {
        let tag = nsString.substring(with: result.range)
        
        // Extract src
        var src = "No src"
        if let srcRegex = try? NSRegularExpression(pattern: "src=\"([^\"]+)\"", options: .caseInsensitive),
           let srcMatch = srcRegex.firstMatch(in: tag, options: [], range: NSRange(location: 0, length: (tag as NSString).length)) {
            src = (tag as NSString).substring(with: srcMatch.range(at: 1))
        }
        
        // Extract alt
        var alt = "No alt"
        if let altRegex = try? NSRegularExpression(pattern: "alt=\"([^\"]+)\"", options: .caseInsensitive),
           let altMatch = altRegex.firstMatch(in: tag, options: [], range: NSRange(location: 0, length: (tag as NSString).length)) {
            alt = (tag as NSString).substring(with: altMatch.range(at: 1))
        }
        
        outputText += "\(idx + 1). Src: \(src)\n   Alt: \(alt)\n\n"
    }
    
    // Ensure output directory exists
    try? FileManager.default.createDirectory(atPath: "/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main/tmp", withIntermediateDirectories: true, attributes: nil)
    try outputText.write(toFile: outputPath, atomically: true, encoding: .utf8)
    print("Successfully parsed and saved image list to tmp/images_list.txt")
} catch {
    print("Error parsing HTML: \(error)")
}

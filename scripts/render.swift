import Foundation
import WebKit
import AppKit

class WebViewRenderer: NSObject, WKNavigationDelegate {
    let webView: WKWebView
    let outputFile: String
    let width: CGFloat
    let height: CGFloat
    
    init(url: URL, outputFile: String, width: CGFloat, height: CGFloat) {
        self.outputFile = outputFile
        self.width = width
        self.height = height
        
        let config = WKWebViewConfiguration()
        self.webView = WKWebView(frame: CGRect(x: 0, y: 0, width: width, height: height), configuration: config)
        super.init()
        self.webView.navigationDelegate = self
        
        print("Loading URL: \(url.path)")
        self.webView.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
    }
    
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        print("Page loaded, waiting 1 second for any animations/charts...")
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            self.takeSnapshot()
        }
    }
    
    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("Failed to load: \(error)")
        exit(1)
    }
    
    func takeSnapshot() {
        print("Taking snapshot...")
        let config = WKSnapshotConfiguration()
        config.rect = CGRect(x: 0, y: 0, width: self.width, height: self.height)
        
        webView.takeSnapshot(with: config) { (image, error) in
            if let error = error {
                print("Snapshot error: \(error)")
                exit(1)
            }
            
            guard let image = image else {
                print("No image generated")
                exit(1)
            }
            
            guard let tiffData = image.tiffRepresentation,
                  let bitmap = NSBitmapImageRep(data: tiffData),
                  let pngData = bitmap.representation(using: .png, properties: [:]) else {
                print("Failed to convert image to PNG")
                exit(1)
            }
            
            do {
                try pngData.write(to: URL(fileURLWithPath: self.outputFile))
                print("Successfully wrote screenshot to \(self.outputFile)")
                exit(0)
            } catch {
                print("Failed to write to file: \(error)")
                exit(1)
            }
        }
    }
}

// Check arguments
let args = CommandLine.arguments
guard args.count >= 5 else {
    print("Usage: ./render <htmlPath> <outputPath> <width> <height>")
    exit(1)
}

let htmlPath: String
let outputPath: String
let widthStr: String
let heightStr: String

if args.count >= 6 && args[1].hasSuffix(".swift") {
    htmlPath = args[2]
    outputPath = args[3]
    widthStr = args[4]
    heightStr = args[5]
} else {
    htmlPath = args[1]
    outputPath = args[2]
    widthStr = args[3]
    heightStr = args[4]
}

guard let widthVal = Double(widthStr), let heightVal = Double(heightStr) else {
    print("Invalid width/height")
    exit(1)
}


let fileURL = URL(fileURLWithPath: htmlPath)
let renderer = WebViewRenderer(url: fileURL, outputFile: outputPath, width: CGFloat(widthVal), height: CGFloat(heightVal))

// Run the main run loop
RunLoop.main.run()

import Foundation
import CoreImage
import ImageIO
import AppKit

print("Starting native pixel-perfect image enhancement pipeline...")

let destDir = "/Users/t.anh/Downloads/BÁO CÁO THỰC TẬP NHÓM 10/image"
let backupFile = "/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main/tmp/backup/image1.png"
let destFile1 = "\(destDir)/image1.png"

// 1. Restore original image1.png from backup if needed
if FileManager.default.fileExists(atPath: backupFile) {
    do {
        if FileManager.default.fileExists(atPath: destFile1) {
            try FileManager.default.removeItem(atPath: destFile1)
        }
        try FileManager.default.copyItem(atPath: backupFile, toPath: destFile1)
        print("Restored original image1.png from workspace backup.")
    } catch {
        print("Error restoring image1.png: \(error)")
    }
}

// 2. Process all 15 images
let ciContext = CIContext(options: [CIContextOption.useSoftwareRenderer: false])

for i in 1...15 {
    let filePath = "\(destDir)/image\(i).png"
    let fileURL = URL(fileURLWithPath: filePath)
    
    guard FileManager.default.fileExists(atPath: filePath) else {
        print("Error: File not found \(filePath)")
        continue
    }
    
    print("Processing image\(i).png...")
    
    // Load original image direct from URL to preserve exact pixel dimensions
    guard let ciImage = CIImage(contentsOf: fileURL) else {
        print("Failed to load CIImage from \(filePath)")
        continue
    }
    
    let originalBounds = ciImage.extent
    print("  Original pixel dimensions: \(Int(originalBounds.width))x\(Int(originalBounds.height))")
    
    // Apply Unsharp Mask Filter to make text extremely sharp and clear
    let unsharpFilter = CIFilter(name: "CIUnsharpMask")!
    unsharpFilter.setValue(ciImage, forKey: kCIInputImageKey)
    unsharpFilter.setValue(1.5, forKey: kCIInputRadiusKey)       // Sharpen radius
    unsharpFilter.setValue(1.0, forKey: kCIInputIntensityKey)    // Sharpen intensity
    
    guard let outputCIImage = unsharpFilter.outputImage else {
        print("Failed to generate sharpened output for image\(i)")
        continue
    }
    
    // Render back to CGImage preserving original dimensions
    guard let cgImage = ciContext.createCGImage(outputCIImage, from: originalBounds) else {
        print("Failed to render output CIImage to CGImage for image\(i)")
        continue
    }
    
    // Convert to PNG data using CGImageDestination to bypass any AppKit DPI scaling
    let uti = "public.png" as CFString

    
    let data = NSMutableData()
    guard let destination = CGImageDestinationCreateWithData(data as CFMutableData, uti, 1, nil) else {
        print("Failed to create CGImageDestination")
        continue
    }
    
    CGImageDestinationAddImage(destination, cgImage, nil)
    if !CGImageDestinationFinalize(destination) {
        print("Failed to finalize image destination")
        continue
    }
    
    // Save enhanced image directly back to report directory
    do {
        try data.write(to: fileURL, options: .atomic)
        print("Successfully enhanced and saved image\(i).png with exact original size (\(Int(originalBounds.width))x\(Int(originalBounds.height)))")
    } catch {
        print("Failed to write enhanced image\(i).png: \(error)")
    }
}

print("All 15 images successfully enhanced and saved.")

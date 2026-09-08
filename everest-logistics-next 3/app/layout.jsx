import './globals.css';import Header from '@/components/Header';import Footer from '@/components/Footer';
export const metadata={title:{default:'Everest Logistics',template:'%s | Everest Logistics'},description:'Giải pháp vận chuyển quốc tế, hải quan và logistics trọn gói cho doanh nghiệp.'};
export default function RootLayout({children}){return <html lang="vi"><body><Header/>{children}<Footer/></body></html>}

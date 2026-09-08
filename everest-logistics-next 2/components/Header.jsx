'use client';
import Link from 'next/link';
import {useState} from 'react';
import {serviceGroups} from '@/lib/services';
export default function Header(){
 const [open,setOpen]=useState(false),[servicesOpen,setServicesOpen]=useState(false);
 return <><div className="topbar"><div className="container"><span>Hotline: <b>0919 108 538</b></span><span>195 đường N, phường Phú Hữu, TP.HCM</span></div></div>
 <header className="nav"><div className="container"><Link className="logo" href="/"><span className="logoMark">▲</span><span>EVEREST<small>LOGISTICS & CUSTOMS</small></span></Link>
 <button className="mobileToggle" onClick={()=>setOpen(!open)} aria-label="Mở menu">☰</button>
 <nav className={open?'menu open':'menu'}><Link href="/">Trang chủ</Link><Link href="/gioi-thieu">Giới thiệu</Link><div className={servicesOpen?'hasMega open':'hasMega'}><Link href="/dich-vu" onClick={e=>{if(innerWidth<=1000){e.preventDefault();setServicesOpen(!servicesOpen)}}}>Dịch vụ ▾</Link><div className="mega">{serviceGroups.map(group=><div key={group.name}><h3>{group.name}</h3>{group.items.map(item=><Link key={item.slug} href={'/dich-vu/'+item.slug}>{item.name}</Link>)}</div>)}</div></div><Link href="/tin-tuc">Tin tức</Link><Link href="/ho-tro">Hỗ trợ khách hàng</Link><Link href="/tuyen-dung">Tuyển dụng</Link><Link href="/lien-he">Liên hệ</Link></nav>
 <Link className="btn btnOrange navCta" href="/bao-gia">Báo giá</Link></div></header></>
}

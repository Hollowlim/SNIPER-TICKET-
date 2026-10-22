import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "YENG | Ticket Sniper", description: "Your next unforgettable night starts here. Mock ticket monitoring dashboard." };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en"><body>{children}</body></html>; }

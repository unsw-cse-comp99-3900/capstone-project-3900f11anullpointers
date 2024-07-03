import Header from "@/components/Header";
import MainBody from "@/components/MainBody";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between">
      <Header />
      <MainBody />
      <Footer />
    </main>
  );
}

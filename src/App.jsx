import { useState, useEffect } from "react";
import FloatingOrb from "./components/FloatingOrb";
import HeroSection from "./components/HeroSection";
import DescriptionSection from "./components/DescriptionSection";
import StatsStrip from "./components/StatsStrip";
import FormSection from "./components/FormSection";
import Footer from "./components/Footer";

export default function App() {
  const [companyName, setCompanyName] = useState("");
  const [companyUrl, setCompanyUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const scrollToForm = () => {
    document.getElementById("generator").scrollIntoView({ behavior: "smooth" });
  };

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   setLoading(true);
  //   setSuccess(false);
  //   setTimeout(() => {
  //     setLoading(false);
  //     setSuccess(true);
  //   }, 2000);
  // };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);

    try {
      const response = await fetch("/generate-brochure", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          companyName: companyName,
          companyUrl: companyUrl,
        }),
      });

      // ❗ important: check for backend errors
      if (!response.ok) {
        throw new Error("Failed to generate brochure");
      }

      // ✅ receive PDF blob
      const blob = await response.blob();

      // ✅ create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${companyName}_brochure.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setSuccess(true);
    } catch (err) {
      console.error(err);
      alert("Error generating brochure. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-x-hidden bg-gradient-to-br from-rose-50 via-white to-violet-100 font-sans">
      <FloatingOrb className="w-96 h-96 bg-violet-300 top-[-80px] left-[-80px]" />
      <FloatingOrb className="w-80 h-80 bg-rose-200 top-40 right-[-60px]" />
      <FloatingOrb className="w-72 h-72 bg-sky-200 bottom-60 left-20" />
      <FloatingOrb className="w-64 h-64 bg-fuchsia-200 bottom-20 right-20" />

      <HeroSection mounted={mounted} scrollToForm={scrollToForm} />

      <div className="relative z-10 w-full max-w-5xl mx-auto px-6">
        <div className="h-px bg-gradient-to-r from-transparent via-violet-200 to-transparent" />
      </div>

      <DescriptionSection />
      <StatsStrip />

      <div className="relative z-10 w-full max-w-5xl mx-auto px-6 mt-12">
        <div className="h-px bg-gradient-to-r from-transparent via-rose-200 to-transparent" />
      </div>

      <FormSection
        companyName={companyName}
        setCompanyName={setCompanyName}
        companyUrl={companyUrl}
        setCompanyUrl={setCompanyUrl}
        loading={loading}
        success={success}
        setSuccess={setSuccess}
        handleSubmit={handleSubmit}
      />

      <Footer />
    </div>
  );
}

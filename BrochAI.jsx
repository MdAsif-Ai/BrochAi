import { useState, useEffect } from "react";

const FloatingOrb = ({ className }) => (
  <div
    className={`absolute rounded-full blur-3xl opacity-30 pointer-events-none ${className}`}
  />
);

export default function BrochAI() {
  const [companyName, setCompanyName] = useState("");
  const [companyUrl, setCompanyUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
    }, 2000);
  };

  const scrollToForm = () => {
    document.getElementById("generator").scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="relative min-h-screen overflow-x-hidden bg-gradient-to-br from-rose-50 via-white to-violet-100 font-sans">
      {/* Decorative blobs */}
      <FloatingOrb className="w-96 h-96 bg-violet-300 top-[-80px] left-[-80px]" />
      <FloatingOrb className="w-80 h-80 bg-rose-200 top-40 right-[-60px]" />
      <FloatingOrb className="w-72 h-72 bg-sky-200 bottom-60 left-20" />
      <FloatingOrb className="w-64 h-64 bg-fuchsia-200 bottom-20 right-20" />

      {/* Hero Section */}
      <section className="relative z-10 flex flex-col items-center justify-center text-center px-6 pt-28 pb-24">
        <div
          className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-violet-200 shadow-sm text-xs font-semibold tracking-widest text-violet-600 uppercase mb-8 transition-all duration-700 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}`}
        >
          <span className="w-2 h-2 rounded-full bg-violet-500 animate-pulse" />
          Powered by AI
        </div>

        <h1
          className={`text-5xl md:text-7xl font-extrabold leading-tight tracking-tight text-gray-900 max-w-4xl transition-all duration-700 delay-100 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"}`}
          style={{ fontFamily: "'Georgia', serif" }}
        >
          Create Stunning{" "}
          <span className="bg-gradient-to-r from-violet-600 via-fuchsia-500 to-rose-500 bg-clip-text text-transparent">
            AI‑Powered
          </span>{" "}
          Brochures in Seconds
        </h1>

        <p
          className={`mt-6 text-lg md:text-xl text-gray-500 max-w-2xl leading-relaxed transition-all duration-700 delay-200 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"}`}
        >
          Turn your company information into a beautifully designed,
          investor-ready PDF — instantly.
        </p>

        <p
          className={`mt-4 text-sm text-gray-400 max-w-lg transition-all duration-700 delay-300 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"}`}
        >
          Simply enter your company name and website URL. Our AI engine scans
          your data and assembles a professional, print-ready brochure tailored
          to your brand in moments.
        </p>

        <button
          onClick={scrollToForm}
          className={`mt-10 px-8 py-4 rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-500 text-white font-bold text-base shadow-lg shadow-violet-200 hover:scale-105 hover:shadow-xl hover:shadow-violet-300 transition-all duration-300 active:scale-95 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"} transition-all duration-700 delay-400`}
        >
          Generate Your Brochure ↓
        </button>
      </section>

      {/* Divider */}
      <div className="relative z-10 w-full max-w-5xl mx-auto px-6">
        <div className="h-px bg-gradient-to-r from-transparent via-violet-200 to-transparent" />
      </div>

      {/* Description Section */}
      <section className="relative z-10 py-24 px-6">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <p className="text-gray-600 text-lg leading-relaxed">
            <span className="font-semibold text-gray-800">
              BrochAI's intelligent engine
            </span>{" "}
            automatically analyzes your company data — pulling key details from
            your website, extracting your value proposition, and structuring
            everything into a coherent, compelling narrative. No guesswork, no
            lengthy briefs. Just results.
          </p>
          <p className="text-gray-600 text-lg leading-relaxed">
            What once took a designer{" "}
            <span className="font-semibold text-gray-800">
              hours or even days
            </span>{" "}
            is now done in under a minute. BrochAI eliminates manual layout
            work, tedious formatting, and design revisions — giving your team
            back the time to focus on what matters most.
          </p>
          <p className="text-gray-600 text-lg leading-relaxed">
            Whether you're a{" "}
            <span className="font-semibold text-gray-800">
              startup pitching investors
            </span>
            , a marketer launching a campaign, or an agency serving multiple
            clients — BrochAI produces structured, pixel-perfect brochures with
            zero design skills required. Beautiful by default.
          </p>
        </div>
      </section>

      {/* Stats strip */}
      <section className="relative z-10 py-6 px-6">
        <div className="max-w-3xl mx-auto grid grid-cols-3 gap-6 text-center">
          {[
            { value: "10,000+", label: "Brochures Generated" },
            { value: "< 60s", label: "Average Generation Time" },
            { value: "98%", label: "Satisfaction Rate" },
          ].map(({ value, label }) => (
            <div
              key={label}
              className="bg-white/70 backdrop-blur-sm rounded-2xl py-5 px-4 border border-white shadow-sm"
            >
              <div className="text-2xl font-extrabold bg-gradient-to-r from-violet-600 to-fuchsia-500 bg-clip-text text-transparent">
                {value}
              </div>
              <div className="text-xs text-gray-500 mt-1 font-medium">
                {label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Divider */}
      <div className="relative z-10 w-full max-w-5xl mx-auto px-6 mt-12">
        <div className="h-px bg-gradient-to-r from-transparent via-rose-200 to-transparent" />
      </div>

      {/* Form Section */}
      <section id="generator" className="relative z-10 py-24 px-6">
        <div className="max-w-lg mx-auto">
          <div className="text-center mb-10">
            <h2
              className="text-3xl md:text-4xl font-extrabold text-gray-900 tracking-tight"
              style={{ fontFamily: "'Georgia', serif" }}
            >
              Generate Your Brochure
            </h2>
            <p className="mt-3 text-gray-400 text-sm">
              Fill in the details below. Your AI brochure will be ready in
              seconds.
            </p>
          </div>

          {/* Glass card */}
          <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl shadow-violet-100 border border-white/60 p-8 md:p-10">
            {success ? (
              <div className="flex flex-col items-center justify-center py-10 text-center gap-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center shadow-lg shadow-violet-200">
                  <svg
                    className="w-8 h-8 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
                <h3 className="text-2xl font-extrabold text-gray-900">
                  Your Brochure is Ready!
                </h3>
                <p className="text-gray-500 text-sm max-w-xs">
                  Your AI-generated brochure for{" "}
                  <span className="font-semibold text-violet-600">
                    {companyName}
                  </span>{" "}
                  has been created successfully.
                </p>
                <button
                  onClick={() => {
                    setSuccess(false);
                    setCompanyName("");
                    setCompanyUrl("");
                  }}
                  className="mt-2 px-6 py-2.5 rounded-xl border border-violet-200 text-violet-600 text-sm font-semibold hover:bg-violet-50 transition-colors duration-200"
                >
                  Create Another
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <label
                    htmlFor="companyName"
                    className="block text-sm font-semibold text-gray-700"
                  >
                    Company Name
                  </label>
                  <input
                    id="companyName"
                    type="text"
                    required
                    placeholder="e.g. Acme Technologies"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    disabled={loading}
                    className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-violet-400 focus:border-transparent transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="companyUrl"
                    className="block text-sm font-semibold text-gray-700"
                  >
                    Company Website URL
                  </label>
                  <input
                    id="companyUrl"
                    type="url"
                    required
                    placeholder="https://www.yourcompany.com"
                    value={companyUrl}
                    onChange={(e) => setCompanyUrl(e.target.value)}
                    disabled={loading}
                    className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-violet-400 focus:border-transparent transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-4 rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-500 text-white font-bold text-sm tracking-wide shadow-md shadow-violet-200 hover:shadow-lg hover:shadow-violet-300 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:scale-100 disabled:hover:shadow-md flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <svg
                        className="w-4 h-4 animate-spin"
                        viewBox="0 0 24 24"
                        fill="none"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        />
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                        />
                      </svg>
                      Generating...
                    </>
                  ) : (
                    "Generate My Brochure"
                  )}
                </button>

                <p className="text-center text-xs text-gray-400">
                  Generation takes approximately 30–60 seconds.
                </p>
              </form>
            )}
          </div>
        </div>
      </section>

      {/* Trust line */}
      <section className="relative z-10 py-6 px-6 text-center">
        <p className="text-xs text-gray-400 tracking-wide">
          Trusted by{" "}
          <span className="font-semibold text-gray-500">10,000+ companies</span>{" "}
          worldwide &nbsp;·&nbsp; No credit card required &nbsp;·&nbsp; Cancel
          anytime
        </p>
      </section>

      {/* Footer */}
      <footer className="relative z-10 py-10 px-6 text-center border-t border-gray-100 mt-6">
        <p className="text-xs text-gray-400">
          © 2026 BrochAI. All rights reserved.
        </p>
      </footer>
    </div>
  );
}

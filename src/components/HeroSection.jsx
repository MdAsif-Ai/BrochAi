export default function HeroSection({ mounted, scrollToForm }) {
  return (
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
        Simply enter your company name and website URL. Our AI engine scans your
        data and assembles a professional, print-ready brochure tailored to your
        brand in moments.
      </p>

      <button
        onClick={scrollToForm}
        className={`mt-10 px-8 py-4 rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-500 text-white font-bold text-base shadow-lg shadow-violet-200 hover:scale-105 hover:shadow-xl hover:shadow-violet-300 transition-all duration-300 active:scale-95 ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"} transition-all duration-700 delay-400`}
      >
        Generate Your Brochure ↓
      </button>
    </section>
  );
}

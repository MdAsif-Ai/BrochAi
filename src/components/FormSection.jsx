export default function FormSection({
  companyName,
  setCompanyName,
  companyUrl,
  setCompanyUrl,
  loading,
  success,
  setSuccess,
  handleSubmit,
}) {
  return (
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
  );
}

const stats = [
  { value: "10,000+", label: "Brochures Generated" },
  { value: "< 60s", label: "Average Generation Time" },
  { value: "98%", label: "Satisfaction Rate" },
];

export default function StatsStrip() {
  return (
    <section className="relative z-10 py-6 px-6">
      <div className="max-w-3xl mx-auto grid grid-cols-3 gap-6 text-center">
        {stats.map(({ value, label }) => (
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
  );
}

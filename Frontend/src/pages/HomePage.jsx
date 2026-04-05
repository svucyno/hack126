import { NavLink } from 'react-router-dom'

export default function HomePage() {
  const features = [
    {
      icon: '🎨',
      title: 'Colour Theory Engine',
      desc: 'A 6-step science-backed engine built on complementary and analogous colour rules — every outfit is mathematically coherent.',
    },
    {
      icon: '🦾',
      title: 'Claude Vision AI',
      desc: 'Claude Vision API reads every item for type, pattern, formality, and occasion — so nothing ends up mismatched.',
    },
    {
      icon: '🏾',
      title: 'Skin Tone Aware',
      desc: 'The Monk Scale 1–7 selector ensures every outfit genuinely flatters your complexion through reflectance science.',
    },
    {
      icon: '✂️',
      title: 'Anchor Feature',
      desc: "Upload a favourite piece — the engine builds the entire look around it, preserving what you already love.",
    },
    {
      icon: '🪼',
      title: '2D Figure Preview',
      desc: 'See outfits on an interactive SVG figure in your skin tone, with real cloth texture on the anchor slot.',
    },
    {
      icon: '🪔',
      title: 'Ethnic Wear First',
      desc: 'Kurtas, dupattas, juttis — treated as first-class categories with culturally accurate figure representation.',
    },
  ]

  const modules = [
    {
      num: '01',
      title: 'Outfit Suggester',
      desc: 'Upload your wardrobe, select your skin tone and occasion. Get AI-scored, colour-harmonious outfits with a 2D figure preview.',
      link: '/outfit',
      cta: 'Build Your Outfit',
    },
    {
      num: '02',
      title: 'Style Me',
      desc: 'No wardrobe upload needed. Just your skin tone and the occasion — curated suggestions in seconds.',
      link: '/style-me',
      cta: 'Try Style Me',
    },
    {
      num: '03',
      title: 'Fashion Analyser',
      desc: 'Upload any outfit photo. Receive an AI letter grade A–D, what works, and three specific improvement tips.',
      link: '/analyser',
      cta: 'Analyse an Outfit',
    },
  ]

  return (
    <div>
      {/* ── Hero ── */}
      <section className="hero">
        <div className="hero-tag">✦ &nbsp;AI-Powered Outfit Intelligence</div>
        <h1>
          Dress Smarter,<br />
          <em>Not Harder.</em>
        </h1>
        <p>
          DripFit builds complete, colour-harmonious outfits from your
          wardrobe — scientifically matched to your skin tone and the
          occasion you're dressing for.
        </p>
        <div className="hero-actions">
          <a href="/accounts/google/login/" className="btn btn-primary" style={{ padding: '14px 36px', fontSize: '1rem' }}>
            Get Started — It's Free
          </a>
          <NavLink to="/style-me" className="btn btn-secondary" style={{ padding: '14px 30px', fontSize: '1rem' }}>
            Try Style Me →
          </NavLink>
        </div>
      </section>

      {/* ── Feature Grid ── */}
      <section className="container" style={{ paddingBottom: 80 }}>
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <h2 className="section-title">Built on Science, Worn with Confidence</h2>
          <p className="section-sub">Every component of DripFit is grounded in colour theory and skin-tone science.</p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(290px, 1fr))', gap: 20 }}>
          {features.map((f) => (
            <div
              className="card fade-up"
              key={f.title}
              style={{ display: 'flex', flexDirection: 'column', gap: 14 }}
            >
              <div style={{
                width: 46, height: 46, borderRadius: '10px',
                background: 'rgba(201,169,110,0.14)', border: '1px solid rgba(201,169,110,0.3)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '1.4rem',
              }}>
                {f.icon}
              </div>
              <h3 style={{
                fontFamily: 'var(--font-display)', fontSize: '1.15rem',
                fontWeight: 600, letterSpacing: '0.02em', color: 'var(--ink)',
              }}>
                {f.title}
              </h3>
              <p style={{ color: 'var(--ink-muted)', fontSize: '0.88rem', lineHeight: 1.7 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Three Modules ── */}
      <section style={{
        background: 'var(--surface-1)',
        borderTop: '1px solid var(--surface-3)',
        borderBottom: '1px solid var(--surface-3)',
        padding: '80px 0',
      }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: 52 }}>
            <h2 className="section-title">Three Powerful Modules</h2>
            <p className="section-sub">One platform — every styling need covered.</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(310px, 1fr))', gap: 24 }}>
            {modules.map((m) => (
              <div
                key={m.num}
                className="fade-up"
                style={{
                  background: 'var(--ivory)', border: '1px solid var(--surface-3)',
                  borderRadius: 'var(--radius-xl)', padding: '36px 30px',
                  display: 'flex', flexDirection: 'column', gap: 0,
                  boxShadow: 'var(--shadow-sm)',
                  transition: 'var(--trans-fast)',
                }}
              >
                <div style={{
                  fontFamily: 'var(--font-display)', fontSize: '4rem', fontWeight: 300,
                  color: 'rgba(201,169,110,0.3)', lineHeight: 1, marginBottom: 16,
                  letterSpacing: '-0.02em',
                }}>
                  {m.num}
                </div>
                <h3 style={{
                  fontFamily: 'var(--font-display)', fontSize: '1.4rem',
                  fontWeight: 600, letterSpacing: '0.03em',
                  color: 'var(--ink)', marginBottom: 12,
                }}>
                  {m.title}
                </h3>
                <p style={{
                  color: 'var(--ink-muted)', fontSize: '0.9rem',
                  lineHeight: 1.7, marginBottom: 28, flex: 1,
                }}>
                  {m.desc}
                </p>
                <NavLink to={m.link} className="btn btn-gold btn-sm" style={{ alignSelf: 'flex-start' }}>
                  {m.cta} →
                </NavLink>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Footer nudge ── */}
      <section className="container" style={{ padding: '60px 28px', textAlign: 'center' }}>
        <p style={{
          fontFamily: 'var(--font-display)', fontStyle: 'italic',
          fontSize: '1.1rem', color: 'var(--ink-muted)', marginBottom: 24,
        }}>
          Your wardrobe is already enough. DripFit just helps it work harder.
        </p>
        <a href="/accounts/google/login/" className="btn btn-primary">
          Start Styling for Free
        </a>
      </section>
    </div>
  )
}

export default {
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  css: ['@/styles/global.css'],
  pages: true,
  app: {
    head: {
      title: "Doppelgan-car - Find Your Car Twin 🚗",
      meta: [
        { name: "description", content: "Upload your image and discover which car matches your personality!" },
        { name: "keywords", content: "car match, AI car matching, car personality test" },
        { name: "author", content: "Your Name or Company" },
        { property: "og:title", content: "Doppelgan-Car - Find Your Car Twin" },
        { property: "og:description", content: "Upload your image and see what car suits you best." },
        { property: "og:image", content: "/Doppelgan-Car.png" },
        { property: "og:type", content: "website" }
      ],
      link: [
        { rel: "icon", type: "image/png", href: "/favicon.ico" }, // Change favicon
        { rel: "apple-touch-icon", href: "/favicon.ico" } // Apple devices
      ]
    }
  }
};
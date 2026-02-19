import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Dobot API v3",
  description: "Documentation for the dobot_api_v3 package",
  themeConfig: {
    nav: [
      { text: "The Basics", link: "/getting-started/installation" },
      { text: "Tutorial", link: "/tutorial/basic-motion" },
      { text: "Reference", link: "/reference/" },
      { text: "Changelog", link: "/changelog" },
      { text: "Dev Guide", link: "/development/contributing" }
    ],
    sidebar: [
      {
        text: "The Basics",
        items: [
          { text: "Installation", link: "/getting-started/installation" },
          { text: "Quick Start", link: "/getting-started/quick-start" },
          { text: "Architecture", link: "/getting-started/architecture" }
        ]
      },
      {
        text: "Tutorial",
        items: [
          { text: "Basic Motion", link: "/tutorial/basic-motion" },
          { text: "Feedback and Monitoring", link: "/tutorial/feedback-monitoring" },
          { text: "I/O and Modbus", link: "/tutorial/io-and-modbus" },
          { text: "Alarm I18n", link: "/tutorial/i18n" }
        ]
      },
      {
        text: "Reference",
        items: [
          { text: "Overview", link: "/reference/" },
          { text: "Generated API Overview", link: "/reference/api/index" },
          { text: "Generated API Modules", link: "/reference/api/modules" },
          { text: "Command Patterns", link: "/reference/command-patterns" },
          { text: "Deprecations", link: "/reference/deprecations" },
          { text: "Feedback Fields", link: "/reference/feedback-fields" }
        ]
      },
      {
        text: "Development",
        items: [
          { text: "Contributing", link: "/development/contributing" },
          { text: "Testing", link: "/development/testing" },
          { text: "Release", link: "/development/release" }
        ]
      }
    ]
  }
});

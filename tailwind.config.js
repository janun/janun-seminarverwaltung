module.exports = {
  important: true,
  theme: {
    fontFamily: {
      sans: ["Cabin", "sans-serif"]
    },
    customForms: theme => ({
      default: {
        "input, textarea, multiselect, select, checkbox, radio": {
          backgroundColor: theme("colors.gray.100"),
          borderColor: theme("colors.gray.300"),
          "&:disabled": {
            cursor: "not-allowed",
            borderColor: theme("colors.gray.100")
          },
          "&.is-invalid": {
            borderColor: theme("colors.red.400")
          }
        },
        "input, textarea, multiselect, select": {
          borderRadius: theme('borderRadius.md'),
        },
        "checkbox, radio": {
          color: theme("colors.gray.700")
        },
        select: {
          iconColor: theme('colors.gray.700'),
        },
        textarea: {
          resize: "none"
        }
      }
    }),
    extend: {
      borderRadius: {
        md: "6px"
      },
      colors: {
        green: {
          50: "#fcfefb",
          100: "#f6fff1",
          200: "#d8f2d8",
          300: "#aee1a5",
          400: "#81c155",
          500: "#3a9d00",
          600: "#308701",
          700: "#2b7b03",
          800: "#236707",
          900: "#1a4614"
        },
        "gray-20": "#fdfdfd",
        "gray-150": "#f4f8fa",
        "white-75": "rgba(255, 255, 255, 0.75)"
      },
      maxWidth: {
        xxs: "10rem"
      },
      spacing: {
        "1.5": "0.375rem"
      },
      screens: {
        xxl: "1600px"
      }
    }
  },
  variants: {
    boxShadow: ["responsive", "hover", "focus", "focus-within"],
    textColor: ["responsive", "hover", "focus", "group-hover"],
  },
  plugins: [require("@tailwindcss/custom-forms")]
};

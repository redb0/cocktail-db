/*!
 * Minimal theme switcher
 *
 * Pico.css - https://picocss.com
 * Copyright 2019-2024 - Licensed under MIT
 */

const themeSwitcher = {
    // Config
    _scheme: "light",
    // menuTarget: "details.dropdown",
    buttonsTarget: "button[data-theme-switcher]",
    buttonAttribute: "data-theme-switcher",
    rootAttribute: "data-theme",
    localStorageKey: "picoPreferredColorScheme",
  
    // Init
    init() {
      this.scheme = this.schemeFromLocalStorage;
      this.initSwitchers();
      this.toggleIcon = this.scheme;
    },

    switchTheme(scheme) {
      this.scheme = scheme === "dark" ? "light" : "dark";
      // this.applyScheme();
      // this.schemeToLocalStorage();
    },

    set toggleIcon(scheme) {
      if (scheme === "light") {
        document.querySelector("#theme-toggle")?.classList.add("theme-toggle--toggled");
      } else {
        document.querySelector("#theme-toggle")?.classList.remove("theme-toggle--toggled");
      }
    },
  
    // Get color scheme from local storage
    get schemeFromLocalStorage() {
      return window.localStorage?.getItem(this.localStorageKey) ?? this._scheme;
    },
  
    // Preferred color scheme
    get preferredColorScheme() {
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    },
  
    // Init switchers
    initSwitchers() {
      const buttons = document.querySelectorAll(this.buttonsTarget);
      buttons.forEach((button) => {
        button.setAttribute(this.buttonAttribute, this._scheme);
      });
      buttons.forEach((button) => {
        button.addEventListener(
          "click",
          (event) => {
            event.preventDefault();
            // Set scheme
            this.switchTheme(button.getAttribute(this.buttonAttribute));
            // Close dropdown
            // document.querySelector(this.menuTarget)?.removeAttribute("open");
            button.setAttribute(this.buttonAttribute, this._scheme);
            this.toggleIcon = this.scheme;
          },
          false
        );
      });
    },

    // Set scheme
    set scheme(scheme) {
      // if (scheme == "auto") {
      // this._scheme = this.preferredColorScheme;
      // } else if (scheme == "dark" || scheme == "light") {
      this._scheme = scheme;
      // }
      this.applyScheme();
      this.schemeToLocalStorage();
    },
  
    // Get scheme
    get scheme() {
      return this._scheme;
    },
  
    // Apply scheme
    applyScheme() {
      document.querySelector("html")?.setAttribute(this.rootAttribute, this.scheme);
    },
  
    // Store scheme to local storage
    schemeToLocalStorage() {
      window.localStorage?.setItem(this.localStorageKey, this.scheme);
    },

    
  };
  
  // Init
  themeSwitcher.init();
  
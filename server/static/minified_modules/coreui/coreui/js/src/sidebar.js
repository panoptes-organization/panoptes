import $ from 'jquery'
import PerfectScrollbar from 'perfect-scrollbar'
import getStyle from './utilities/get-style'
import toggleClasses from './toggle-classes'

/**
 * --------------------------------------------------------------------------
 * CoreUI (v2.1.12): sidebar.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

const Sidebar = (($) => {
  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  const NAME                = 'sidebar'
  const VERSION             = '2.1.12'
  const DATA_KEY            = 'coreui.sidebar'
  const EVENT_KEY           = `.${DATA_KEY}`
  const DATA_API_KEY        = '.data-api'
  const JQUERY_NO_CONFLICT  = $.fn[NAME]

  const Default = {
    transition : 400
  }

  const ClassName = {
    ACTIVE              : 'active',
    BRAND_MINIMIZED     : 'brand-minimized',
    NAV_DROPDOWN_TOGGLE : 'nav-dropdown-toggle',
    OPEN                : 'open',
    SIDEBAR_FIXED       : 'sidebar-fixed',
    SIDEBAR_MINIMIZED   : 'sidebar-minimized',
    SIDEBAR_OFF_CANVAS  : 'sidebar-off-canvas'
  }

  const Event = {
    CLICK         : 'click',
    DESTROY       : 'destroy',
    INIT          : 'init',
    LOAD_DATA_API : `load${EVENT_KEY}${DATA_API_KEY}`,
    TOGGLE        : 'toggle',
    UPDATE        : 'update'
  }

  const Selector = {
    BODY                 : 'body',
    BRAND_MINIMIZER      : '.brand-minimizer',
    NAV_DROPDOWN_TOGGLE  : '.nav-dropdown-toggle',
    NAV_DROPDOWN_ITEMS   : '.nav-dropdown-items',
    NAV_ITEM             : '.nav-item',
    NAV_LINK             : '.nav-link',
    NAV_LINK_QUERIED     : '.nav-link-queried',
    NAVIGATION_CONTAINER : '.sidebar-nav',
    NAVIGATION           : '.sidebar-nav > .nav',
    SIDEBAR              : '.sidebar',
    SIDEBAR_MINIMIZER    : '.sidebar-minimizer',
    SIDEBAR_TOGGLER      : '.sidebar-toggler',
    SIDEBAR_SCROLL       : '.sidebar-scroll'
  }

  const ShowClassNames = [
    'sidebar-show',
    'sidebar-sm-show',
    'sidebar-md-show',
    'sidebar-lg-show',
    'sidebar-xl-show'
  ]

  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  class Sidebar {
    constructor(element) {
      this._element = element
      this.mobile = false
      this.ps = null
      this.perfectScrollbar(Event.INIT)
      this.setActiveLink()
      this._breakpointTest = this._breakpointTest.bind(this)
      this._clickOutListener = this._clickOutListener.bind(this)
      this._addEventListeners()
      this._addMediaQuery()
    }

    // Getters

    static get VERSION() {
      return VERSION
    }

    // Public

    perfectScrollbar(event) {
      if (typeof PerfectScrollbar !== 'undefined') {
        const classList = document.body.classList
        if (event === Event.INIT && !classList.contains(ClassName.SIDEBAR_MINIMIZED)) {
          this.ps = this.makeScrollbar()
        }

        if (event === Event.DESTROY) {
          this.destroyScrollbar()
        }

        if (event === Event.TOGGLE) {
          if (classList.contains(ClassName.SIDEBAR_MINIMIZED)) {
            this.destroyScrollbar()
          } else {
            this.destroyScrollbar()
            this.ps = this.makeScrollbar()
          }
        }

        if (event === Event.UPDATE && !classList.contains(ClassName.SIDEBAR_MINIMIZED)) {
          // ToDo: Add smooth transition
          setTimeout(() => {
            this.destroyScrollbar()
            this.ps = this.makeScrollbar()
          }, Default.transition)
        }
      }
    }

    makeScrollbar() {
      let container = Selector.SIDEBAR_SCROLL

      if (document.querySelector(container) === null) {
        container = Selector.NAVIGATION_CONTAINER

        if (document.querySelector(container) === null) {
          return null
        }
      }

      const ps = new PerfectScrollbar(document.querySelector(container), {
        suppressScrollX: true
      })
      // ToDo: find real fix for ps rtl
      ps.isRtl = false
      return ps
    }

    destroyScrollbar() {
      if (this.ps) {
        this.ps.destroy()
        this.ps = null
      }
    }

    setActiveLink() {
      $(Selector.NAVIGATION).find(Selector.NAV_LINK).each((key, value) => {
        let link = value
        let cUrl

        if (link.classList.contains(Selector.NAV_LINK_QUERIED)) {
          cUrl = String(window.location)
        } else {
          cUrl = String(window.location).split('?')[0]
        }

        if (cUrl.substr(cUrl.length - 1) === '#') {
          cUrl = cUrl.slice(0, -1)
        }
        if ($($(link))[0].href === cUrl) {
          $(link).addClass(ClassName.ACTIVE).parents(Selector.NAV_DROPDOWN_ITEMS).add(link).each((key, value) => {
            link = value
            $(link).parent().addClass(ClassName.OPEN)
          })
        }
      })
    }

    // Private

    _addMediaQuery() {
      const sm = getStyle('--breakpoint-sm')
      if (!sm) {
        return
      }
      const smVal = parseInt(sm, 10) - 1
      const mediaQueryList = window.matchMedia(`(max-width: ${smVal}px)`)

      this._breakpointTest(mediaQueryList)

      mediaQueryList.addListener(this._breakpointTest)
    }

    _breakpointTest(e) {
      this.mobile = Boolean(e.matches)
      this._toggleClickOut()
    }

    _clickOutListener(event) {
      if (!this._element.contains(event.target)) { // or use: event.target.closest(Selector.SIDEBAR) === null
        event.preventDefault()
        event.stopPropagation()
        this._removeClickOut()
        document.body.classList.remove('sidebar-show')
      }
    }

    _addClickOut() {
      document.addEventListener(Event.CLICK, this._clickOutListener, true)
    }

    _removeClickOut() {
      document.removeEventListener(Event.CLICK, this._clickOutListener, true)
    }

    _toggleClickOut() {
      if (this.mobile && document.body.classList.contains('sidebar-show')) {
        document.body.classList.remove('aside-menu-show')
        this._addClickOut()
      } else {
        this._removeClickOut()
      }
    }

    _addEventListeners() {
      $(document).on(Event.CLICK, Selector.BRAND_MINIMIZER, (event) => {
        event.preventDefault()
        event.stopPropagation()
        $(Selector.BODY).toggleClass(ClassName.BRAND_MINIMIZED)
      })

      $(document).on(Event.CLICK, Selector.NAV_DROPDOWN_TOGGLE, (event) => {
        event.preventDefault()
        event.stopPropagation()
        const dropdown = event.target
        $(dropdown).parent().toggleClass(ClassName.OPEN)
        this.perfectScrollbar(Event.UPDATE)
      })

      $(document).on(Event.CLICK, Selector.SIDEBAR_MINIMIZER, (event) => {
        event.preventDefault()
        event.stopPropagation()
        $(Selector.BODY).toggleClass(ClassName.SIDEBAR_MINIMIZED)
        this.perfectScrollbar(Event.TOGGLE)
      })

      $(document).on(Event.CLICK, Selector.SIDEBAR_TOGGLER, (event) => {
        event.preventDefault()
        event.stopPropagation()
        const toggle = event.currentTarget.dataset ? event.currentTarget.dataset.toggle : $(event.currentTarget).data('toggle')
        toggleClasses(toggle, ShowClassNames)
        this._toggleClickOut()
      })

      $(`${Selector.NAVIGATION} > ${Selector.NAV_ITEM} ${Selector.NAV_LINK}:not(${Selector.NAV_DROPDOWN_TOGGLE})`).on(Event.CLICK, () => {
        this._removeClickOut()
        document.body.classList.remove('sidebar-show')
      })
    }

    // Static

    static _jQueryInterface() {
      return this.each(function () {
        const $element = $(this)
        let data = $element.data(DATA_KEY)

        if (!data) {
          data = new Sidebar(this)
          $element.data(DATA_KEY, data)
        }
      })
    }
  }

  /**
   * ------------------------------------------------------------------------
   * Data Api implementation
   * ------------------------------------------------------------------------
   */

  $(window).on(Event.LOAD_DATA_API, () => {
    const sidebar = $(Selector.SIDEBAR)
    Sidebar._jQueryInterface.call(sidebar)
  })

  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME] = Sidebar._jQueryInterface
  $.fn[NAME].Constructor = Sidebar
  $.fn[NAME].noConflict = () => {
    $.fn[NAME] = JQUERY_NO_CONFLICT
    return Sidebar._jQueryInterface
  }

  return Sidebar
})($)

export default Sidebar

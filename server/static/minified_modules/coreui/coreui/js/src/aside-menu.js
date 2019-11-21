import $ from 'jquery'
import toggleClasses from './toggle-classes'

/**
 * --------------------------------------------------------------------------
 * CoreUI (v2.1.12): aside-menu.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

const AsideMenu = (($) => {
  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  const NAME                = 'aside-menu'
  const VERSION             = '2.1.12'
  const DATA_KEY            = 'coreui.aside-menu'
  const EVENT_KEY           = `.${DATA_KEY}`
  const DATA_API_KEY        = '.data-api'
  const JQUERY_NO_CONFLICT  = $.fn[NAME]

  const Event = {
    CLICK         : 'click',
    LOAD_DATA_API : `load${EVENT_KEY}${DATA_API_KEY}`,
    TOGGLE        : 'toggle'
  }

  const Selector = {
    BODY               : 'body',
    ASIDE_MENU         : '.aside-menu',
    ASIDE_MENU_TOGGLER : '.aside-menu-toggler'
  }

  const ShowClassNames = [
    'aside-menu-show',
    'aside-menu-sm-show',
    'aside-menu-md-show',
    'aside-menu-lg-show',
    'aside-menu-xl-show'
  ]

  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  class AsideMenu {
    constructor(element) {
      this._element = element
      this._addEventListeners()
    }

    // Getters

    static get VERSION() {
      return VERSION
    }

    // Private

    _addEventListeners() {
      $(document).on(Event.CLICK, Selector.ASIDE_MENU_TOGGLER, (event) => {
        event.preventDefault()
        event.stopPropagation()
        const toggle = event.currentTarget.dataset ? event.currentTarget.dataset.toggle : $(event.currentTarget).data('toggle')
        toggleClasses(toggle, ShowClassNames)
      })
    }

    // Static

    static _jQueryInterface() {
      return this.each(function () {
        const $element = $(this)
        let data = $element.data(DATA_KEY)

        if (!data) {
          data = new AsideMenu(this)
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
    const asideMenu = $(Selector.ASIDE_MENU)
    AsideMenu._jQueryInterface.call(asideMenu)
  })

  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME] = AsideMenu._jQueryInterface
  $.fn[NAME].Constructor = AsideMenu
  $.fn[NAME].noConflict = () => {
    $.fn[NAME] = JQUERY_NO_CONFLICT
    return AsideMenu._jQueryInterface
  }

  return AsideMenu
})($)

export default AsideMenu

import $ from 'jquery'

/**
 * --------------------------------------------------------------------------
 * CoreUI (v2.1.12): ajax-load.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */


const AjaxLoad = (($) => {
  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  const NAME                       = 'ajaxLoad'
  const VERSION                    = '2.1.12'
  const DATA_KEY                   = 'coreui.ajaxLoad'
  const JQUERY_NO_CONFLICT         = $.fn[NAME]

  const ClassName = {
    ACTIVE      : 'active',
    NAV_PILLS   : 'nav-pills',
    NAV_TABS    : 'nav-tabs',
    OPEN        : 'open',
    VIEW_SCRIPT : 'view-script'
  }

  const Event = {
    CLICK : 'click'
  }

  const Selector = {
    HEAD         : 'head',
    NAV_DROPDOWN : '.sidebar-nav .nav-dropdown',
    NAV_LINK     : '.sidebar-nav .nav-link',
    NAV_ITEM     : '.sidebar-nav .nav-item',
    VIEW_SCRIPT  : '.view-script'
  }

  const Default = {
    defaultPage       : 'main.html',
    errorPage         : '404.html',
    subpagesDirectory : 'views/'
  }

  class AjaxLoad {
    constructor(element, config) {
      this._config = this._getConfig(config)
      this._element = element

      const url = location.hash.replace(/^#/, '')

      if (url !== '') {
        this.setUpUrl(url)
      } else {
        this.setUpUrl(this._config.defaultPage)
      }
      this._addEventListeners()
    }

    // Getters

    static get VERSION() {
      return VERSION
    }

    static get Default() {
      return Default
    }

    // Public

    loadPage(url) {
      const element = this._element
      const config = this._config

      const loadScripts = (src, element = 0) => {
        const script = document.createElement('script')
        script.type = 'text/javascript'
        script.src = src[element]
        script.className = ClassName.VIEW_SCRIPT
        // eslint-disable-next-line no-multi-assign
        script.onload = script.onreadystatechange = function () {
          if (!this.readyState || this.readyState === 'complete') {
            if (src.length > element + 1) {
              loadScripts(src, element + 1)
            }
          }
        }
        const body = document.getElementsByTagName('body')[0]
        body.appendChild(script)
      }

      $.ajax({
        type : 'GET',
        url : config.subpagesDirectory + url,
        dataType : 'html',
        beforeSend() {
          $(Selector.VIEW_SCRIPT).remove()
        },
        success(result) {
          const wrapper = document.createElement('div')
          wrapper.innerHTML = result

          const scripts = Array.from(wrapper.querySelectorAll('script')).map((script) => script.attributes.getNamedItem('src').nodeValue)

          wrapper.querySelectorAll('script').forEach((script) => script.parentNode.removeChild(script))

          $('body').animate({
            scrollTop: 0
          }, 0)
          $(element).html(wrapper)
          if (scripts.length) {
            loadScripts(scripts)
          }
          window.location.hash = url
        },
        error() {
          window.location.href = config.errorPage
        }
      })
    }

    setUpUrl(url) {
      $(Selector.NAV_LINK).removeClass(ClassName.ACTIVE)
      $(Selector.NAV_DROPDOWN).removeClass(ClassName.OPEN)

      $(`${Selector.NAV_DROPDOWN}:has(a[href="${url.replace(/^\//, '').split('?')[0]}"])`).addClass(ClassName.OPEN)
      $(`${Selector.NAV_ITEM} a[href="${url.replace(/^\//, '').split('?')[0]}"]`).addClass(ClassName.ACTIVE)

      this.loadPage(url)
    }

    loadBlank(url) {
      window.open(url)
    }

    loadTop(url) {
      window.location = url
    }

    // Private

    _getConfig(config) {
      config = {
        ...Default,
        ...config
      }
      return config
    }

    _addEventListeners() {
      $(document).on(Event.CLICK, `${Selector.NAV_LINK}[href!="#"]`, (event) => {
        event.preventDefault()
        event.stopPropagation()

        if (event.currentTarget.target === '_top') {
          this.loadTop(event.currentTarget.href)
        } else if (event.currentTarget.target === '_blank') {
          this.loadBlank(event.currentTarget.href)
        } else {
          this.setUpUrl(event.currentTarget.getAttribute('href'))
        }
      })
    }

    // Static

    static _jQueryInterface(config) {
      return this.each(function () {
        let data = $(this).data(DATA_KEY)
        const _config = typeof config === 'object' && config

        if (!data) {
          data = new AjaxLoad(this, _config)
          $(this).data(DATA_KEY, data)
        }
      })
    }
  }

  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME] = AjaxLoad._jQueryInterface
  $.fn[NAME].Constructor = AjaxLoad
  $.fn[NAME].noConflict = () => {
    $.fn[NAME] = JQUERY_NO_CONFLICT
    return AjaxLoad._jQueryInterface
  }

  return AjaxLoad
})($)

export default AjaxLoad

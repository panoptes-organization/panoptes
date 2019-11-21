/**
 * --------------------------------------------------------------------------
 * CoreUI (v2.1.12): toggle-classes.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */

const removeClasses = (classNames) => classNames.map((className) => document.body.classList.contains(className)).indexOf(true) !== -1

const toggleClasses = (toggleClass, classNames) => {
  const breakpoint = classNames.indexOf(toggleClass)
  const newClassNames = classNames.slice(0, breakpoint + 1)

  if (removeClasses(newClassNames)) {
    newClassNames.map((className) => document.body.classList.remove(className))
  } else {
    document.body.classList.add(toggleClass)
  }
}

export default toggleClasses

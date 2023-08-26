"use strict";
(self["webpackChunk_datalayer_jupyter_docker"] = self["webpackChunk_datalayer_jupyter_docker"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_signaling-webpack_sharing_consume_default-8bfbc6"],{

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!*********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \*********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".dla-Container {\n    overflow-y: visible;\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;IACI,mBAAmB;AACvB","sourcesContent":[".dla-Container {\n    overflow-y: visible;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!**********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \**********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../../../../node_modules/css-loader/dist/cjs.js!./base.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../icons/react/data2/esm/WhaleSpoutingIcon.js":
/*!********************************************************!*\
  !*** ../../icons/react/data2/esm/WhaleSpoutingIcon.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function WhaleSpoutingIcon({
  title,
  titleId,
  size,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    viewBox: "0 0 72 72",
    fill: "currentColor",
    "aria-hidden": "true",
    ref: svgRef,
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("g", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    strokeWidth: 2
  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#61b2e4",
    d: "M22.3 44.828c.621 2.675 1.87 5.243 3.527 7.752.906 1.371 2.583.787 2.977-.809.34-.88.542-1.899.633-2.959"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#61b2e4",
    strokeMiterlimit: 10,
    d: "M46.638 14.502c-.694.206-.997 3.416-.95 4.523.132 3.044 5.278 3.092 2.848 6.4-10.496 11.84-26.393-3.784-34.527 3.661C12.765 40.522 30.867 56.536 45 47c8.206-5.537 10.46-14.795 11.082-20.096.441-1.146 1.465-1.403 3.284-1.898 5.193-1.46 4.904-4.3 4.953-8.127-2.359 2.857-4.907 1.8-6.823 1.728-1.106-.004-2.181 1.244-2.857 1.795-.09-.63-.226-1.476-.832-2.178-1.505-1.744-4.947-.76-6.4-2.877-.232-.535-.44-.792-.623-.845a.252.252 0 00-.145 0z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#d0cfce",
    d: "M57 26.054l-.21.065-.81 1.47c.005-.04.015-.09.02-.129v-.04c-.019.083-.042.16-.06.243l-1.438 2.616a32.465 32.465 0 01-1.428 4.705c-5.536 8.899-15.765 7.784-22.539 3.277-3.774-2.511-8.69-7.273-11.914-7.67-2.12-.26-4.48 1.017-4.064 3.139l-.733 1.29c1.532 4.412 5.001 8.68 9.372 11.7 6.375 4.406 14.943 6.121 22.389 1.098C53.865 42.23 56.272 33.136 57 27.617v-1.563z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#61b2e4",
    d: "M35.89 40.827c.522 5.619 3.525 9.756 8.005 13.242 1.298 1.01 2.697-.082 2.56-1.72.188-4.36-2.664-10.671-5.707-10.676"
  })), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("g", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    strokeWidth: 2,
    color: "#000"
  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M19.455 13.84a3.965 3.965 0 00-1.81.252c-1.172.452-2.235 1.38-3.231 2.69a1 1 0 101.592 1.208c.848-1.115 1.687-1.773 2.36-2.033.672-.26 1.146-.211 1.704.158 1.117.74 2.432 3.329 2.852 8a1 1 0 101.992-.177c-.445-4.944-1.64-8.1-3.738-9.49a3.767 3.767 0 00-1.721-.607zM31.482 12.607a4.3 4.3 0 00-1.738.229c-2.288.798-3.91 3.46-4.098 7.806a1 1 0 101.998.086c.168-3.897 1.521-5.571 2.76-6.004 1.239-.432 2.798.19 3.904 1.986a1 1 0 101.703-1.048c-1.095-1.78-2.787-2.928-4.529-3.054zM23.621 9.898a1 1 0 00-.938 1.309c.235.76.48 1.328.524 2.291a1 1 0 101.998-.092c-.06-1.28-.417-2.158-.611-2.789a1 1 0 00-.973-.718zM47.197 39.408a1 1 0 00-.453.102c-1.869.878-3.898 1.231-5.961 1.166a1 1 0 10-.063 2c2.335.074 4.69-.33 6.875-1.358a1 1 0 00-.398-1.91z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M35.881 39.812a1 1 0 00-.986 1.107c.55 5.926 3.774 10.351 8.386 13.94.924.718 2.183.746 3.012.158.82-.582 1.232-1.608 1.152-2.711.085-2.4-.605-5.13-1.738-7.38-.573-1.135-1.258-2.146-2.066-2.917-.809-.772-1.785-1.332-2.89-1.334a1 1 0 10-.005 2c.415 0 .938.23 1.514.78.576.549 1.163 1.388 1.66 2.374.994 1.972 1.621 4.536 1.537 6.479a1 1 0 00.002.127c.044.518-.164.839-.324.953s-.252.185-.625-.106c-4.35-3.384-7.13-7.236-7.623-12.548a1 1 0 00-1.006-.922z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M18.742 29.598c-1.31-.161-2.647.13-3.693.857s-1.775 2.066-1.465 3.526a1 1 0 101.957-.416c-.147-.69.085-1.075.648-1.467.563-.392 1.483-.617 2.309-.516 1.191.147 3.21 1.326 5.28 2.854s4.24 3.35 6.202 4.656a22.217 22.217 0 005.559 2.672 1 1 0 10.605-1.906 20.253 20.253 0 01-5.054-2.43c-1.812-1.205-3.986-3.02-6.125-4.6s-4.191-2.98-6.223-3.23z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    strokeMiterlimit: 10,
    d: "M47.088 13.537a1.3 1.3 0 00-.709.002 1 1 0 00-.566.436c-.055.063-.178.107-.22.167-.147.217-.239.43-.32.653-.16.447-.267.946-.351 1.467-.168 1.04-.237 2.116-.207 2.802.045 1.042.554 1.876 1.117 2.465.564.59 1.183 1.003 1.637 1.37.454.365.681.655.726.82.044.158.033.433-.423 1.072-2.458 2.752-5.114 3.86-7.993 4.154-2.894.296-6.015-.279-9.136-1.02-3.122-.74-6.23-1.643-9.176-1.888-2.947-.245-5.828.218-8.11 2.307a1 1 0 00-.318.628c-.533 4.896 2.093 10.255 6.252 14.473s9.927 7.332 16.002 7.454a1 1 0 10.04-2c-5.412-.107-10.767-2.95-14.619-6.856-3.716-3.77-5.902-8.477-5.664-12.406 1.723-1.406 3.753-1.814 6.25-1.606 2.65.22 5.697 1.089 8.88 1.844 3.18.755 6.51 1.4 9.804 1.062 3.293-.337 6.544-1.716 9.324-4.851a1 1 0 00.059-.07c.707-.964.996-1.956.755-2.827-.24-.87-.853-1.405-1.398-1.845-.545-.44-1.085-.815-1.447-1.194-.363-.379-.544-.692-.565-1.172-.018-.42.04-1.503.184-2.396.024-.15.06-.234.088-.371.979 1.078 2.314 1.477 3.437 1.693 1.255.241 2.207.454 2.653.97.395.458.51 1.052.597 1.667a1 1 0 001.623.633c.424-.346.83-.768 1.246-1.09.416-.322.794-.478.971-.479.79.034 1.96.328 3.324.23.783-.055 1.619-.353 2.448-.831-.046.948-.138 1.795-.409 2.431-.459 1.08-1.326 1.923-3.756 2.606-.901.245-1.651.43-2.335.773-.687.344-1.307.937-1.612 1.729a1 1 0 00-.058.242c-.504 4.29-2.123 11.218-7.155 16.445a1 1 0 101.442 1.387c5.413-5.625 7.105-12.838 7.662-17.381.13-.325.24-.445.615-.633.39-.195 1.062-.388 1.975-.637a1 1 0 00.007-.002c2.764-.777 4.348-2.084 5.055-3.746.707-1.662.603-3.445.627-5.33a1 1 0 00-1.771-.649c-1.029 1.246-1.91 1.533-2.877 1.602-.967.07-2.013-.194-3.137-.236a1 1 0 00-.033-.002c-.93-.004-1.64.462-2.205.9-.064.05-.084.077-.145.127-.15-.356-.288-.717-.586-1.062-1.06-1.229-2.583-1.396-3.789-1.627-1.196-.23-2.05-.468-2.53-1.15-.236-.555-.442-1.037-1.18-1.253z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M22.281 43.816a1 1 0 00-.928 1.238c.656 2.826 1.963 5.498 3.666 8.077.646.976 1.828 1.407 2.803 1.115.96-.288 1.68-1.125 1.959-2.192.369-.98.585-2.053.68-3.156a1 1 0 10-1.994-.172c-.085.99-.274 1.921-.569 2.684a1 1 0 00-.039.12c-.125.506-.423.743-.611.8s-.298.093-.559-.301c-1.612-2.44-2.802-4.903-3.388-7.428a1 1 0 00-1.02-.785z"
  })));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(WhaleSpoutingIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../icons/react/data2/esm/WhaleSpoutingIconLabIcon.js":
/*!***************************************************************!*\
  !*** ../../icons/react/data2/esm/WhaleSpoutingIconLabIcon.js ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components/lib/icon/labicon */ "../../../node_modules/@jupyterlab/ui-components/lib/icon/labicon.js");
/* harmony import */ var _WhaleSpoutingIcon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./WhaleSpoutingIcon.svg */ "../../icons/react/data2/esm/WhaleSpoutingIcon.svg");


const whaleSpoutingIconLabIcon = new _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: '@datalayer/icons:whale-spouting',
    svgstr: _WhaleSpoutingIcon_svg__WEBPACK_IMPORTED_MODULE_1__,
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (whaleSpoutingIconLabIcon);

/***/ }),

/***/ "../../icons/react/eggs/esm/PirateSkull2Icon.js":
/*!******************************************************!*\
  !*** ../../icons/react/eggs/esm/PirateSkull2Icon.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function PirateSkull2Icon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    viewBox: "0 0 512 512",
    fill: colored ? 'currentColor' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('currentColor') ? 'white' : 'currentColor'),
    "aria-hidden": "true",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M256 31.203c-96 .797-117.377 76.692-79.434 135.133-6.397 6.534-10.344 15.886-.566 25.664 16 16 32 16 39.852 32.42h80.296C304 208 320 208 336 192c9.778-9.778 5.831-19.13-.566-25.664C373.377 107.896 352 32 256 31.203zm-42.146 101.049c.426-.003.862.007 1.306.03 28.404 1.442 40.84 59.718-10.83 51.095-10.412-1.738-17.355-50.963 9.524-51.125zm84.292 0c26.88.162 19.936 49.387 9.524 51.125C256 192 268.436 133.724 296.84 132.28c.444-.022.88-.032 1.306-.03zM32 144c7.406 88.586 64.475 175.544 156.623 236.797 17.959-7.251 35.767-15.322 50.424-23.877C180.254 319.737 104.939 255.465 32 144zm448 0C359.2 328.605 231.863 383.797 183.908 400.797c3.177 5.374 5.997 10.98 8.711 16.432 3.878 7.789 7.581 15.251 11.184 20.986A517.457 517.457 0 00256 417.973l.168.076a884.617 884.617 0 009.652-4.65C391.488 353.263 471.156 249.79 480 144zm-224 27.725l20.074 40.15L256 199.328l-20.074 12.547L256 171.725zm-65.604 57.11l15.76 51.042s31.268 24.92 49.844 24.92 49.844-24.92 49.844-24.92l15.76-51.041-27.086 19.236-8.063 16.248S267.35 279.547 256 279.547c-11.35 0-30.455-15.227-30.455-15.227l-8.063-16.248-27.086-19.236zm-59.984 152.976a32.548 32.548 0 00-2.375.027l.856 17.978c6.36-.302 10.814 2.416 16.11 8.64 5.298 6.222 10.32 15.707 15.24 25.589 4.918 9.882 9.707 20.12 16.122 28.45 6.415 8.327 16.202 15.446 27.969 13.89l-2.36-17.844c-4.094.541-6.78-1.099-11.349-7.031-4.57-5.933-9.275-15.46-14.268-25.489-4.992-10.029-10.297-20.604-17.644-29.234-6.888-8.09-16.556-14.686-28.3-14.976zm251.176 0c-11.745.29-21.413 6.885-28.3 14.976-7.348 8.63-12.653 19.205-17.645 29.234-4.993 10.03-9.698 19.556-14.268 25.489-4.57 5.932-7.255 7.572-11.35 7.031l-2.359 17.844c11.767 1.556 21.554-5.563 27.969-13.89 6.415-8.33 11.204-18.568 16.123-28.45 4.919-9.882 9.94-19.367 15.238-25.59 5.297-6.223 9.75-8.941 16.111-8.639l.856-17.978a32.853 32.853 0 00-2.375-.027zm-55.928 18.107c-13.97 10.003-30.13 18.92-47.424 27.478a524.868 524.868 0 0029.961 10.819c3.603-5.735 7.306-13.197 11.184-20.986 2.714-5.453 5.534-11.058 8.71-16.432-.77-.273-1.62-.586-2.43-.879zm-191.808 23.371l-27.67 10.352 7.904 31.771 36.424-11.707c-1.418-2.814-2.81-5.649-4.207-8.457-4.048-8.131-8.169-15.961-12.451-21.959zm244.296 0c-4.282 5.998-8.403 13.828-12.45 21.959-1.399 2.808-2.79 5.643-4.208 8.457l36.424 11.707 7.904-31.771-27.67-10.352zM78.271 435.438a9.632 9.632 0 00-1.32.12 6.824 6.824 0 00-1.217.313c-11.544 4.201-25.105 18.04-21.648 29.828 3.07 10.472 19.675 13.359 30.492 11.916 3.828-.51 8.415-3.761 12.234-7.086l-8.124-32.648c-3.238-1.285-7.214-2.528-10.417-2.443zm355.458 0c-3.203-.085-7.179 1.158-10.416 2.443l-8.125 32.648c3.819 3.325 8.406 6.576 12.234 7.086 10.817 1.443 27.422-1.444 30.492-11.916 3.457-11.788-10.104-25.627-21.648-29.828a6.824 6.824 0 00-1.217-.312 9.632 9.632 0 00-1.32-.122z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(PirateSkull2Icon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "./lib/JupyterDocker.js":
/*!******************************!*\
  !*** ./lib/JupyterDocker.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ThemeProvider.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/BaseStyles.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/UnderlineNav2/index.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data2/esm/WhaleSpoutingIcon.js");
/* harmony import */ var _tabs_ImagesTab__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/ImagesTab */ "./lib/tabs/ImagesTab.js");
/* harmony import */ var _tabs_ContainersTab__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/ContainersTab */ "./lib/tabs/ContainersTab.js");
/* harmony import */ var _tabs_AboutTab__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/AboutTab */ "./lib/tabs/AboutTab.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");









const JupyterDocker = (props) => {
    const [tab, setTab] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(1);
    const [version, setVersion] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('config')
            .then(data => {
            setVersion(data.version);
        })
            .catch(reason => {
            console.error(`The Jupyter Server jupyter_docker extension appears to be missing.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { "aria-current": "page", onSelect: e => { e.preventDefault(); setTab(1); }, children: "Images" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { onSelect: e => { e.preventDefault(); setTab(2); }, children: "Containers" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { icon: () => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_7__["default"], { colored: true }), onSelect: e => { e.preventDefault(); setTab(3); }, children: "About" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { m: 3, children: [tab === 1 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_ImagesTab__WEBPACK_IMPORTED_MODULE_8__["default"], {}), tab === 2 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_ContainersTab__WEBPACK_IMPORTED_MODULE_9__["default"], {}), tab === 3 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_AboutTab__WEBPACK_IMPORTED_MODULE_10__["default"], { version: version })] })] }) }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JupyterDocker);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyter_docker', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IJupyterDocker": () => (/* binding */ IJupyterDocker),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _datalayer_icons_react_data2_WhaleSpoutingIconLabIcon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @datalayer/icons-react/data2/WhaleSpoutingIconLabIcon */ "../../icons/react/data2/esm/WhaleSpoutingIconLabIcon.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./store */ "./lib/store/index.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");









const IJupyterDocker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyter-docker:plugin');
/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-jupyter-docker-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the @datalayer/jupyter-docker extension.
 */
const plugin = {
    id: '@datalayer/jupyter-docker:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    provides: IJupyterDocker,
    activate: (app, palette, settingRegistry, launcher) => {
        const jupyterDocker = {
            timer: _store__WEBPACK_IMPORTED_MODULE_5__.timer,
            TimerView: _store__WEBPACK_IMPORTED_MODULE_5__.TimerView,
        };
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'Show Jupyter Docker',
            label: 'Jupyter Docker',
            icon: _datalayer_icons_react_data2_WhaleSpoutingIconLabIcon__WEBPACK_IMPORTED_MODULE_6__["default"],
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_7__.JupyterDockerWidget(app);
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.MainAreaWidget({ content });
                widget.title.label = 'Jupyter Docker';
                widget.title.icon = _datalayer_icons_react_data2_WhaleSpoutingIconLabIcon__WEBPACK_IMPORTED_MODULE_6__["default"];
                app.shell.add(widget, 'main');
            }
        });
        const category = 'Datalayer';
        palette.addItem({ command, category });
        if (launcher) {
            launcher.add({
                command,
                category,
                rank: 3,
            });
        }
        console.log('JupyterLab extension @datalayer/jupyter-docker is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('@datalayer/jupyter-docker settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for @datalayer/jupyter-docker.', reason);
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_8__.requestAPI)('config')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The Jupyter Server extension jupyter_docker appears to be missing.\n${reason}`);
        });
        return jupyterDocker;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/store/index.js":
/*!****************************!*\
  !*** ./lib/store/index.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Timer": () => (/* binding */ Timer),
/* harmony export */   "TimerView": () => (/* binding */ TimerView),
/* harmony export */   "timer": () => (/* binding */ timer)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var mobx__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! mobx */ "webpack/sharing/consume/default/mobx/mobx?346a");
/* harmony import */ var mobx__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(mobx__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var mobx_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! mobx-react */ "webpack/sharing/consume/default/mobx-react/mobx-react");
/* harmony import */ var mobx_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(mobx_react__WEBPACK_IMPORTED_MODULE_2__);



class Timer {
    secondsPassed = 0;
    constructor() {
        (0,mobx__WEBPACK_IMPORTED_MODULE_1__.makeAutoObservable)(this);
    }
    reset() {
        this.secondsPassed = 0;
    }
    increaseTimer() {
        this.secondsPassed += 1;
    }
}
const timer = new Timer();
setInterval(() => {
    timer.increaseTimer();
}, 1000);
const TimerView = (0,mobx_react__WEBPACK_IMPORTED_MODULE_2__.observer)(({ timer }) => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("button", { onClick: () => timer.reset(), children: ["Jupyter Docker: ", timer.secondsPassed] })));


/***/ }),

/***/ "./lib/tabs/AboutTab.js":
/*!******************************!*\
  !*** ./lib/tabs/AboutTab.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Pagehead/Pagehead.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Label/Label.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Link/Link.js");
/* harmony import */ var _datalayer_icons_react_eggs_PirateSkull2Icon__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @datalayer/icons-react/eggs/PirateSkull2Icon */ "../../icons/react/eggs/esm/PirateSkull2Icon.js");




const AboutTab = (props) => {
    const { version } = props;
    const [pirate, setPirate] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { as: "h3", children: ["Jupyter Docker", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { marginLeft: 1 }, children: version })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: "\uD83E\uDE90 \uD83D\uDC33 Manage Docker from Jupyter." }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { mt: 3, children: !pirate ?
                    (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("img", { src: "https://assets.datalayer.tech/releases/0.2.0-omalley.png", onClick: e => setPirate(true) })
                    :
                        (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_eggs_PirateSkull2Icon__WEBPACK_IMPORTED_MODULE_6__["default"], { size: 500, onClick: e => setPirate(false) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://datalayer.tech/docs/releases/0.2.0-omalley", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "O'Malley release" }) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://github.com/datalayer/jupyter-docker", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "Source code" }) }) })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (AboutTab);


/***/ }),

/***/ "./lib/tabs/ContainersTab.js":
/*!***********************************!*\
  !*** ./lib/tabs/ContainersTab.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./../handler */ "./lib/handler.js");




const Containers = () => {
    const [containers, setContainers] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('containers')
            .then(data => {
            setContainers(data.containers);
        })
            .catch(reason => {
            console.error(`The Jupyter Server jupyter_docker extension appears to be missing.\n${reason}`);
        });
    });
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: "Docker Containers" }), containers && containers.map(container => {
                    return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: container.id });
                })] }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Containers);


/***/ }),

/***/ "./lib/tabs/ImagesTab.js":
/*!*******************************!*\
  !*** ./lib/tabs/ImagesTab.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/index.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/DataTable.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./../handler */ "./lib/handler.js");





const Images = () => {
    const [images, setImages] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('images')
            .then(data => {
            const images = JSON.parse(data.images);
            console.log('---', images);
            const dockerImages = images.map((image, id) => {
                return {
                    id,
                    ...image
                };
            });
            setImages(dockerImages);
        })
            .catch(reason => {
            console.error(`The Jupyter Server jupyter_docker extension appears to be missing.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Title, { as: "h2", id: "repositories", children: "Docker images" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Subtitle, { as: "p", id: "repositories-subtitle", children: "List of docker images" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.DataTable, { "aria-labelledby": "file-types", "aria-describedby": "file-types-subtitle", data: images, columns: [
                            {
                                header: 'RepoTags',
                                field: 'attrs.RepoTags',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: row.attrs.RepoTags.map(repoTag => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: repoTag })) })
                            },
                            {
                                header: 'Size',
                                field: 'attrs.Size',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.attrs.Size })
                            },
                            {
                                header: 'Os',
                                field: 'attrs.Os',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.attrs.Os })
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Images);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JupyterDockerWidget": () => (/* binding */ JupyterDockerWidget)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _JupyterDocker__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./JupyterDocker */ "./lib/JupyterDocker.js");



class JupyterDockerWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    _app;
    constructor(app) {
        super();
        this._app = app;
        this.addClass('dla-Container');
    }
    render() {
        return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_JupyterDocker__WEBPACK_IMPORTED_MODULE_2__["default"], { app: this._app }) });
    }
}


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "../../icons/react/data2/esm/WhaleSpoutingIcon.svg":
/*!*********************************************************!*\
  !*** ../../icons/react/data2/esm/WhaleSpoutingIcon.svg ***!
  \*********************************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 72 72\" fill=\"currentColor\" aria-hidden=\"true\">\n  <g stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\">\n    <path fill=\"#61b2e4\" d=\"M22.3 44.828c.621 2.675 1.87 5.243 3.527 7.752.906 1.371 2.583.787 2.977-.809.34-.88.542-1.899.633-2.959\"/>\n    <path fill=\"#61b2e4\" stroke-miterlimit=\"10\" d=\"M46.638 14.502c-.694.206-.997 3.416-.95 4.523.132 3.044 5.278 3.092 2.848 6.4-10.496 11.84-26.393-3.784-34.527 3.661C12.765 40.522 30.867 56.536 45 47c8.206-5.537 10.46-14.795 11.082-20.096.441-1.146 1.465-1.403 3.284-1.898 5.193-1.46 4.904-4.3 4.953-8.127-2.359 2.857-4.907 1.8-6.823 1.728-1.106-.004-2.181 1.244-2.857 1.795-.09-.63-.226-1.476-.832-2.178-1.505-1.744-4.947-.76-6.4-2.877-.232-.535-.44-.792-.623-.845a.252.252 0 00-.145 0z\"/>\n    <path fill=\"#d0cfce\" d=\"M57 26.054l-.21.065-.81 1.47c.005-.04.015-.09.02-.129v-.04c-.019.083-.042.16-.06.243l-1.438 2.616a32.465 32.465 0 01-1.428 4.705c-5.536 8.899-15.765 7.784-22.539 3.277-3.774-2.511-8.69-7.273-11.914-7.67-2.12-.26-4.48 1.017-4.064 3.139l-.733 1.29c1.532 4.412 5.001 8.68 9.372 11.7 6.375 4.406 14.943 6.121 22.389 1.098C53.865 42.23 56.272 33.136 57 27.617v-1.563z\"/>\n    <path fill=\"#61b2e4\" d=\"M35.89 40.827c.522 5.619 3.525 9.756 8.005 13.242 1.298 1.01 2.697-.082 2.56-1.72.188-4.36-2.664-10.671-5.707-10.676\"/>\n  </g>\n  <g stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" color=\"#000\">\n    <path d=\"M19.455 13.84a3.965 3.965 0 00-1.81.252c-1.172.452-2.235 1.38-3.231 2.69a1 1 0 101.592 1.208c.848-1.115 1.687-1.773 2.36-2.033.672-.26 1.146-.211 1.704.158 1.117.74 2.432 3.329 2.852 8a1 1 0 101.992-.177c-.445-4.944-1.64-8.1-3.738-9.49a3.767 3.767 0 00-1.721-.607zM31.482 12.607a4.3 4.3 0 00-1.738.229c-2.288.798-3.91 3.46-4.098 7.806a1 1 0 101.998.086c.168-3.897 1.521-5.571 2.76-6.004 1.239-.432 2.798.19 3.904 1.986a1 1 0 101.703-1.048c-1.095-1.78-2.787-2.928-4.529-3.054zM23.621 9.898a1 1 0 00-.938 1.309c.235.76.48 1.328.524 2.291a1 1 0 101.998-.092c-.06-1.28-.417-2.158-.611-2.789a1 1 0 00-.973-.718zM47.197 39.408a1 1 0 00-.453.102c-1.869.878-3.898 1.231-5.961 1.166a1 1 0 10-.063 2c2.335.074 4.69-.33 6.875-1.358a1 1 0 00-.398-1.91z\"/>\n    <path d=\"M35.881 39.812a1 1 0 00-.986 1.107c.55 5.926 3.774 10.351 8.386 13.94.924.718 2.183.746 3.012.158.82-.582 1.232-1.608 1.152-2.711.085-2.4-.605-5.13-1.738-7.38-.573-1.135-1.258-2.146-2.066-2.917-.809-.772-1.785-1.332-2.89-1.334a1 1 0 10-.005 2c.415 0 .938.23 1.514.78.576.549 1.163 1.388 1.66 2.374.994 1.972 1.621 4.536 1.537 6.479a1 1 0 00.002.127c.044.518-.164.839-.324.953s-.252.185-.625-.106c-4.35-3.384-7.13-7.236-7.623-12.548a1 1 0 00-1.006-.922z\"/>\n    <path d=\"M18.742 29.598c-1.31-.161-2.647.13-3.693.857s-1.775 2.066-1.465 3.526a1 1 0 101.957-.416c-.147-.69.085-1.075.648-1.467.563-.392 1.483-.617 2.309-.516 1.191.147 3.21 1.326 5.28 2.854s4.24 3.35 6.202 4.656a22.217 22.217 0 005.559 2.672 1 1 0 10.605-1.906 20.253 20.253 0 01-5.054-2.43c-1.812-1.205-3.986-3.02-6.125-4.6s-4.191-2.98-6.223-3.23z\"/>\n    <path stroke-miterlimit=\"10\" d=\"M47.088 13.537a1.3 1.3 0 00-.709.002 1 1 0 00-.566.436c-.055.063-.178.107-.22.167-.147.217-.239.43-.32.653-.16.447-.267.946-.351 1.467-.168 1.04-.237 2.116-.207 2.802.045 1.042.554 1.876 1.117 2.465.564.59 1.183 1.003 1.637 1.37.454.365.681.655.726.82.044.158.033.433-.423 1.072-2.458 2.752-5.114 3.86-7.993 4.154-2.894.296-6.015-.279-9.136-1.02-3.122-.74-6.23-1.643-9.176-1.888-2.947-.245-5.828.218-8.11 2.307a1 1 0 00-.318.628c-.533 4.896 2.093 10.255 6.252 14.473s9.927 7.332 16.002 7.454a1 1 0 10.04-2c-5.412-.107-10.767-2.95-14.619-6.856-3.716-3.77-5.902-8.477-5.664-12.406 1.723-1.406 3.753-1.814 6.25-1.606 2.65.22 5.697 1.089 8.88 1.844 3.18.755 6.51 1.4 9.804 1.062 3.293-.337 6.544-1.716 9.324-4.851a1 1 0 00.059-.07c.707-.964.996-1.956.755-2.827-.24-.87-.853-1.405-1.398-1.845-.545-.44-1.085-.815-1.447-1.194-.363-.379-.544-.692-.565-1.172-.018-.42.04-1.503.184-2.396.024-.15.06-.234.088-.371.979 1.078 2.314 1.477 3.437 1.693 1.255.241 2.207.454 2.653.97.395.458.51 1.052.597 1.667a1 1 0 001.623.633c.424-.346.83-.768 1.246-1.09.416-.322.794-.478.971-.479.79.034 1.96.328 3.324.23.783-.055 1.619-.353 2.448-.831-.046.948-.138 1.795-.409 2.431-.459 1.08-1.326 1.923-3.756 2.606-.901.245-1.651.43-2.335.773-.687.344-1.307.937-1.612 1.729a1 1 0 00-.058.242c-.504 4.29-2.123 11.218-7.155 16.445a1 1 0 101.442 1.387c5.413-5.625 7.105-12.838 7.662-17.381.13-.325.24-.445.615-.633.39-.195 1.062-.388 1.975-.637a1 1 0 00.007-.002c2.764-.777 4.348-2.084 5.055-3.746.707-1.662.603-3.445.627-5.33a1 1 0 00-1.771-.649c-1.029 1.246-1.91 1.533-2.877 1.602-.967.07-2.013-.194-3.137-.236a1 1 0 00-.033-.002c-.93-.004-1.64.462-2.205.9-.064.05-.084.077-.145.127-.15-.356-.288-.717-.586-1.062-1.06-1.229-2.583-1.396-3.789-1.627-1.196-.23-2.05-.468-2.53-1.15-.236-.555-.442-1.037-1.18-1.253z\"/>\n    <path d=\"M22.281 43.816a1 1 0 00-.928 1.238c.656 2.826 1.963 5.498 3.666 8.077.646.976 1.828 1.407 2.803 1.115.96-.288 1.68-1.125 1.959-2.192.369-.98.585-2.053.68-3.156a1 1 0 10-1.994-.172c-.085.99-.274 1.921-.569 2.684a1 1 0 00-.039.12c-.125.506-.423.743-.611.8s-.298.093-.559-.301c-1.612-2.44-2.802-4.903-3.388-7.428a1 1 0 00-1.02-.785z\"/>\n  </g>\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_signaling-webpack_sharing_consume_default-8bfbc6.d0f9ee4e723c9819ef33.js.map
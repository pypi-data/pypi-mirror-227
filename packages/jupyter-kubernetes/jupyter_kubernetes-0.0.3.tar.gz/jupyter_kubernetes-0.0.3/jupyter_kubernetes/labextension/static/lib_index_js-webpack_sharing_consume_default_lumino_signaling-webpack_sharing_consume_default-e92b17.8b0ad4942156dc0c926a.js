"use strict";
(self["webpackChunk_datalayer_jupyter_kubernetes"] = self["webpackChunk_datalayer_jupyter_kubernetes"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_signaling-webpack_sharing_consume_default-e92b17"],{

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

/***/ "../../icons/react/data2/esm/WheelOfDharmaIcon.js":
/*!********************************************************!*\
  !*** ../../icons/react/data2/esm/WheelOfDharmaIcon.js ***!
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

function WheelOfDharmaIcon({
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
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: "#b399c8",
    d: "M12 12h48v47.83H12z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("g", {
    fill: "none",
    stroke: "#000",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    strokeWidth: 3,
    d: "M51.01 35.99a15 15 0 11-15-15 15 15 0 0115 15z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    strokeWidth: 3,
    d: "M41 36a5 5 0 11-5-5.001A5.001 5.001 0 0141 36zM36 31V19M36 53V41"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    strokeWidth: 2,
    d: "M12 12h48v48H12z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    strokeWidth: 3,
    d: "M41 36h12M19 36h12M39.54 32.46l8.48-8.48M23.98 48.02l8.48-8.48M32.46 32.46l-8.48-8.48M48.02 48.02l-8.48-8.48"
  })));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(WheelOfDharmaIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../../icons/react/data2/esm/WheelOfDharmaIconLabIcon.js":
/*!***************************************************************!*\
  !*** ../../icons/react/data2/esm/WheelOfDharmaIconLabIcon.js ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components/lib/icon/labicon */ "../../../node_modules/@jupyterlab/ui-components/lib/icon/labicon.js");
/* harmony import */ var _WheelOfDharmaIcon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./WheelOfDharmaIcon.svg */ "../../icons/react/data2/esm/WheelOfDharmaIcon.svg");


const wheelOfDharmaIconLabIcon = new _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: '@datalayer/icons:wheel-of-dharma',
    svgstr: _WheelOfDharmaIcon_svg__WEBPACK_IMPORTED_MODULE_1__,
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (wheelOfDharmaIconLabIcon);

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

/***/ "./lib/JupyterKubernetes.js":
/*!**********************************!*\
  !*** ./lib/JupyterKubernetes.js ***!
  \**********************************/
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
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @datalayer/icons-react */ "../../icons/react/data2/esm/WheelOfDharmaIcon.js");
/* harmony import */ var _components_PodsTab__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/PodsTab */ "./lib/components/PodsTab.js");
/* harmony import */ var _components_ServicesTab__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./components/ServicesTab */ "./lib/components/ServicesTab.js");
/* harmony import */ var _components_AboutTab__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./components/AboutTab */ "./lib/components/AboutTab.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");









const JupyterKubernetes = (props) => {
    const [tab, setTab] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(1);
    const [version, setVersion] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('config')
            .then(data => {
            setVersion(data.version);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server jupyter_kubernetes extension.\n${reason}`);
        });
    });
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { "aria-current": "page", onSelect: e => { e.preventDefault(); setTab(1); }, children: "Pods" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { onSelect: e => { e.preventDefault(); setTab(2); }, children: "Services" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.UnderlineNav.Item, { icon: () => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_7__["default"], { colored: true }), onSelect: e => { e.preventDefault(); setTab(3); }, children: "About" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { m: 3, children: [tab === 1 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_PodsTab__WEBPACK_IMPORTED_MODULE_8__["default"], {}), tab === 2 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_ServicesTab__WEBPACK_IMPORTED_MODULE_9__["default"], {}), tab === 3 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_AboutTab__WEBPACK_IMPORTED_MODULE_10__["default"], { version: version })] })] }) }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JupyterKubernetes);


/***/ }),

/***/ "./lib/components/AboutTab.js":
/*!************************************!*\
  !*** ./lib/components/AboutTab.js ***!
  \************************************/
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
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { as: "h3", children: ["Jupyter Kubernetes", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { marginLeft: 1 }, children: version })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: "\uD83E\uDE90 \u2638\uFE0F Manage Kubernetes from Jupyter." }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { mt: 3, children: !pirate ?
                    (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("img", { src: "https://assets.datalayer.tech/releases/0.2.0-omalley.png", onClick: e => setPirate(true) })
                    :
                        (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_eggs_PirateSkull2Icon__WEBPACK_IMPORTED_MODULE_6__["default"], { size: 500, onClick: e => setPirate(false) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://datalayer.tech/docs/releases/0.2.0-omalley", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "O'Malley release" }) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://github.com/datalayer/jupyter-kubernetes", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "Source code" }) }) })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (AboutTab);


/***/ }),

/***/ "./lib/components/PodsTab.js":
/*!***********************************!*\
  !*** ./lib/components/PodsTab.js ***!
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
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/index.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/DataTable.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./../handler */ "./lib/handler.js");





const PodsTab = (props) => {
    const [pods, setPods] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('pods')
            .then(data => {
            const pods = data.pods.map((pod, id) => {
                return {
                    id,
                    ...pod,
                };
            });
            setPods(pods);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server jupyter_kubernetes extension.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Title, { as: "h2", id: "pods", children: "Pods" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Subtitle, { as: "p", id: "pods-subtitle", children: "List of pods" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.DataTable, { "aria-labelledby": "pods", "aria-describedby": "pods-subtitle", data: pods, columns: [
                            {
                                header: 'Name',
                                field: 'metadata.name',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.metadata.name })
                            },
                            {
                                header: 'Namespace',
                                field: 'metadata.namespace',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.metadata.namespace })
                            },
                            {
                                header: 'IP',
                                field: 'status.pod_ip',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.status.pod_ip })
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PodsTab);


/***/ }),

/***/ "./lib/components/ServicesTab.js":
/*!***************************************!*\
  !*** ./lib/components/ServicesTab.js ***!
  \***************************************/
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





const ServicesTab = (props) => {
    const [services, setServices] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('services')
            .then(data => {
            const services = data.services.map((service, id) => {
                return {
                    id,
                    ...service,
                };
            });
            setServices(services);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server jupyter_kubernetes extension.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Title, { as: "h2", id: "services", children: "Services" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Subtitle, { as: "p", id: "services-subtitle", children: "List of services" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.DataTable, { "aria-labelledby": "services", "aria-describedby": "services-subtitle", data: services, columns: [
                            {
                                header: 'Name',
                                field: 'metadata.name',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.metadata.name })
                            },
                            {
                                header: 'Namespace',
                                field: 'metadata.namespace',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.metadata.namespace })
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ServicesTab);


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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyter_kubernetes', // API Namespace
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
/* harmony export */   "IJupyterKubernetes": () => (/* binding */ IJupyterKubernetes),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "jupyterKubernetes": () => (/* binding */ jupyterKubernetes)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _datalayer_jupyter_docker__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/jupyter-docker */ "webpack/sharing/consume/default/@datalayer/jupyter-docker");
/* harmony import */ var _datalayer_jupyter_docker__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyter_docker__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _datalayer_icons_react_data2_WheelOfDharmaIconLabIcon__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @datalayer/icons-react/data2/WheelOfDharmaIconLabIcon */ "../../icons/react/data2/esm/WheelOfDharmaIconLabIcon.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _store__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./store */ "./lib/store/index.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");










const IJupyterKubernetes = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyter-kubernetes:plugin');
const jupyterKubernetes = {
    timer: _store__WEBPACK_IMPORTED_MODULE_6__.timer,
    TimerView: _store__WEBPACK_IMPORTED_MODULE_6__.TimerView,
};
/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-jupyter-kubernetes-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the @datalayer/jupyter-kubernetes extension.
 */
const plugin = {
    id: '@datalayer/jupyter-kubernetes:plugin',
    autoStart: true,
    requires: [_datalayer_jupyter_docker__WEBPACK_IMPORTED_MODULE_4__.IJupyterDocker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    activate: (app, jupyterDocker, palette, settingRegistry, launcher) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'Show Jupyter Kubernetes',
            label: 'Jupyter Kubernetes',
            icon: _datalayer_icons_react_data2_WheelOfDharmaIconLabIcon__WEBPACK_IMPORTED_MODULE_7__["default"],
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_8__.JupyterKubernetesWidget(app, jupyterKubernetes, jupyterDocker);
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.MainAreaWidget({ content });
                widget.title.label = 'Jupyter Kubernetes';
                widget.title.icon = _datalayer_icons_react_data2_WheelOfDharmaIconLabIcon__WEBPACK_IMPORTED_MODULE_7__["default"];
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
        console.log('JupyterLab extension @datalayer/jupyter-kubernetes is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('@datalayer/jupyter-kubernetes settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for @datalayer/jupyter-kubernetes.', reason);
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_9__.requestAPI)('config')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The Jupyter Server extension jupyter_kubernetes appears to be missing.\n${reason}`);
        });
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
/* harmony import */ var mobx__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! mobx */ "../../../node_modules/mobx/dist/mobx.esm.js");
/* harmony import */ var mobx_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! mobx-react */ "../../../node_modules/mobx-react/dist/mobxreact.esm.js");



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
const TimerView = (0,mobx_react__WEBPACK_IMPORTED_MODULE_2__.observer)(({ timer }) => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("button", { onClick: () => timer.reset(), children: ["Jupyter Kubernetes: ", timer.secondsPassed] })));


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JupyterKubernetesWidget": () => (/* binding */ JupyterKubernetesWidget)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _JupyterKubernetes__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./JupyterKubernetes */ "./lib/JupyterKubernetes.js");



class JupyterKubernetesWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    _app;
    constructor(app, jupyterKubernetes, jupyterDocker) {
        super();
        this._app = app;
        this.addClass('dla-Container');
    }
    render() {
        return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_JupyterKubernetes__WEBPACK_IMPORTED_MODULE_2__["default"], { app: this._app }) }));
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

/***/ "../../icons/react/data2/esm/WheelOfDharmaIcon.svg":
/*!*********************************************************!*\
  !*** ../../icons/react/data2/esm/WheelOfDharmaIcon.svg ***!
  \*********************************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 72 72\" fill=\"currentColor\" aria-hidden=\"true\">\n  <path fill=\"#b399c8\" d=\"M12 12h48v47.83H12z\"/>\n  <g fill=\"none\" stroke=\"#000\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n    <path stroke-width=\"3\" d=\"M51.01 35.99a15 15 0 11-15-15 15 15 0 0115 15z\"/>\n    <path stroke-width=\"3\" d=\"M41 36a5 5 0 11-5-5.001A5.001 5.001 0 0141 36zM36 31V19M36 53V41\"/>\n    <path stroke-width=\"2\" d=\"M12 12h48v48H12z\"/>\n    <path stroke-width=\"3\" d=\"M41 36h12M19 36h12M39.54 32.46l8.48-8.48M23.98 48.02l8.48-8.48M32.46 32.46l-8.48-8.48M48.02 48.02l-8.48-8.48\"/>\n  </g>\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_signaling-webpack_sharing_consume_default-e92b17.8b0ad4942156dc0c926a.js.map
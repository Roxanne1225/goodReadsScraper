(this["webpackJsonpreact-app"]=this["webpackJsonpreact-app"]||[]).push([[0],{45:function(e,t,c){},54:function(e,t,c){},55:function(e,t,c){"use strict";c.r(t);var n=c(0),r=c(11),s=c.n(r),i=(c(45),c(15)),j=c(9),o=c(71),a=c(4);var u=function(e){var t=e.setCollectionType;return Object(a.jsx)("div",{children:Object(a.jsxs)(j.a,{children:[Object(a.jsx)(j.a.Toggle,{variant:"success",id:"dropdown-basic",children:"book or author"}),Object(a.jsxs)(j.a.Menu,{children:[Object(a.jsx)(j.a.Item,{onClick:function(){return t("book")},children:"Book"}),Object(a.jsx)(j.a.Item,{onClick:function(){return t("author")},children:"Author"})]})]})})};var b=function(e){var t=Object(n.useState)("book"),c=Object(i.a)(t,2),r=c[0],s=c[1],j=Object(n.useState)("-1"),b=Object(i.a)(j,2),d=b[0],l=b[1];return"GET"===e.operator?Object(a.jsxs)(o.a,{onSubmit:function(){},children:[Object(a.jsxs)(o.a.Field,{children:[Object(a.jsx)(u,{setCollectionType:s}),Object(a.jsxs)("h1",{children:["selected: ",r]})]}),Object(a.jsxs)(o.a.Field,{children:[Object(a.jsx)("input",{type:"number",onChange:function(e){return l(e.target.value)}}),Object(a.jsxs)("h1",{children:["id is: ",d]})]}),Object(a.jsx)(o.a.Button,{content:"Submit"})]}):Object(a.jsx)("h1",{children:"Other"})};c(54);var d=function(){var e=Object(n.useState)("GET"),t=Object(i.a)(e,2),c=t[0],r=t[1];return Object(a.jsxs)("div",{class:"in",children:[Object(a.jsxs)(j.a,{children:[Object(a.jsx)(j.a.Toggle,{variant:"success",id:"dropdown-basic",children:"Dropdown Button"}),Object(a.jsxs)(j.a.Menu,{children:[Object(a.jsx)(j.a.Item,{onClick:function(){return r("GET")},children:"GET"}),Object(a.jsx)(j.a.Item,{onClick:function(){return r("SEARCH")},children:"SEARCH"})]})]}),Object(a.jsx)(b,{operator:c})]})};var l=function(){return Object(a.jsx)("div",{className:"App",children:Object(a.jsx)(d,{})})};s.a.render(Object(a.jsx)(l,{}),document.getElementById("root"))}},[[55,1,2]]]);
//# sourceMappingURL=main.a869703f.chunk.js.map
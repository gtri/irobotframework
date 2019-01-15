*** Variables ***
${CELL_CSS}       .jp-Notebook .jp-Cell:last-of-type .jp-InputArea-editor .CodeMirror
${SPLASH_ID}      jupyterlab-splash
${SPINNER}        css:.jp-Spinner
${CMD_PAL_XPATH}    css:li[data-id="command-palette"]
${CMD_PAL_INPUT}    css:.p-CommandPalette-input
${CMD_PAL_ITEM}    css:.p-CommandPalette-item
${TOP}            //div[@id='jp-top-panel']
${BAR_ITEM}       //div[@class='p-MenuBar-itemLabel']
${CARD_CSS}       .jp-Activity:not(.p-mod-hidden) .jp-LauncherCard
${DOCK}           //div[@id='jp-main-dock-panel']
${CLOSE_TAB}      css:.p-TabBar-tabCloseIcon
${SAVE}           css:.jp-SaveIcon

${JLAB CSS ACTIVE SIDEBAR}  .jp-SideBar .p-TabBar-tab.p-mod-current
${JLAB CSS SIDEBAR TAB}  .jp-SideBar .p-TabBar-tab
${JLAB CSS ACCEPT}  .jp-mod-accept

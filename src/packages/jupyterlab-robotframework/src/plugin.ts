/*
  Copyright (c) 2018 Georgia Tech Research Corporation
  Distributed under the terms of the BSD-3-Clause License
*/

import { JupyterLab, JupyterLabPlugin } from '@jupyterlab/application';

import { PLUGIN_ID } from '.';

import '../style/index.css';

import { defineRobotMode } from './mode';
defineRobotMode();

function activate(app: JupyterLab) {
  console.log(PLUGIN_ID, app);
}

/**
 * Initialization data for the jupyterlab-robotframework extension.
 */
const extension: JupyterLabPlugin<void> = {
  activate,
  autoStart: true,
  id: PLUGIN_ID
};

export default extension;

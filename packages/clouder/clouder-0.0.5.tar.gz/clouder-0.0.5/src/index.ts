import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { MainAreaWidget, ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import icon from '@datalayer/icons-react/data2/CloudGreyIconLabIcon';
import { requestAPI } from './handler';
import { ClouderWidget } from './widget';

import '../style/index.css';

/**
 * The command IDs used by the plugin.
 */
namespace CommandIDs {
  export const create = 'create-clouder-widget';
}

/**
 * Initialization data for the @datalayer/clouder extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@datalayer/clouder:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry, ILauncher],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher
  ) => {
    const { commands } = app;
    const command = CommandIDs.create;
    commands.addCommand(command, {
      caption: 'Show Clouder',
      label: 'Clouder',
      icon,
      execute: () => {
        const content = new ClouderWidget();
        const widget = new MainAreaWidget<ClouderWidget>({ content });
        widget.title.label = 'Clouder';
        widget.title.icon = icon;
        app.shell.add(widget, 'main');
      }
    });
    const category = 'Datalayer';
    palette.addItem({ command, category });
    if (launcher) {
      launcher.add({
        command,
        category,
        rank: 2
      });
    }
    console.log('JupyterLab extension @datalayer/clouder is activated!');
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@datalayer/clouder settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @datalayer/clouder.', reason);
        });
    }
    requestAPI<any>('config')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `Error while accessing the jupyter server extension.\n${reason}`
        );
      });
  }
};

export default plugin;

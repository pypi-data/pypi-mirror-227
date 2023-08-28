import { useState, useEffect } from 'react';
import { ThemeProvider, BaseStyles, Box } from '@primer/react';
import { UnderlineNav } from '@primer/react/drafts';
import { CloudGreyIcon, OvhCloudIcon, AwsIcon } from '@datalayer/icons-react';
import { requestAPI } from './handler';
import ClouderTab from './tabs/ClouderTab';
import OVHTab from './tabs/OVHTab';
import AWSTab from './tabs/AWSTab';
import AboutTab from './tabs/AboutTab';

const Clouder = (): JSX.Element => {
  const [tab, setTab] = useState(1);
  const [version, setVersion] = useState('');
  useEffect(() => {
    requestAPI<any>('config')
    .then(data => {
      setVersion(data.version);
    })
    .catch(reason => {
      console.error(
        `Error while accessing the jupyter server clouder extension.\n${reason}`
      );
    });
  });
  return (
    <>
      <ThemeProvider>
        <BaseStyles>
          <Box style={{maxWidth: 700}}>
            <Box>
              <UnderlineNav>
                <UnderlineNav.Item aria-current="page" icon={CloudGreyIcon} onSelect={e => {e.preventDefault(); setTab(1);}}>
                  Clouder
                </UnderlineNav.Item>
                <UnderlineNav.Item icon={OvhCloudIcon} onSelect={e => {e.preventDefault(); setTab(2);}}>
                  OVHcloud
                </UnderlineNav.Item>
                <UnderlineNav.Item icon={AwsIcon} onSelect={e => {e.preventDefault(); setTab(3);}}>
                  AWS
                </UnderlineNav.Item>
                <UnderlineNav.Item icon={CloudGreyIcon} onSelect={e => {e.preventDefault(); setTab(4);}}>
                  About
                </UnderlineNav.Item>
              </UnderlineNav>
            </Box>
            <Box m={3}>
              {(tab === 1) && <ClouderTab version={version}/>}
              {(tab === 2) && <OVHTab/>}
              {(tab === 3) && <AWSTab/>}
              {(tab === 4) && <AboutTab version={version}/>}
            </Box>
          </Box>
        </BaseStyles>
      </ThemeProvider>
    </>
  );
}

export default Clouder;

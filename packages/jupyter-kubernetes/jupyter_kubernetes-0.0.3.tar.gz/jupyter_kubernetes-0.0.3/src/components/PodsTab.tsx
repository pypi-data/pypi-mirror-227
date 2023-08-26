import { useState, useEffect } from 'react';
import { Box, Text } from '@primer/react';
import { Table, DataTable } from '@primer/react/drafts';
import { JupyterFrontEndProps } from '../JupyterKubernetes';
import { requestAPI } from './../handler';

type Pod = {
  id: number,
  metadata: {
    name: string,
    namespace: string,
  },
  status: {
    pod_ip: string,
  }
}

const PodsTab = (props: JupyterFrontEndProps) => {
  const [pods, setPods] = useState(new Array<Pod>());
  useEffect(() => {
    requestAPI<any>('pods')
    .then(data => {
      const pods = (data.pods as [any]).map((pod, id) => {
        return {
          id,
          ...pod,
        }
      });
      setPods(pods);
    })
    .catch(reason => {
      console.error(
        `Error while accessing the jupyter server jupyter_kubernetes extension.\n${reason}`
      );
    });
  }, []);
  return (
    <>
      <Box>
        <Table.Container>
          <Table.Title as="h2" id="pods">
            Pods
          </Table.Title>
          <Table.Subtitle as="p" id="pods-subtitle">
            List of pods
          </Table.Subtitle>
          <DataTable
            aria-labelledby="pods"
            aria-describedby="pods-subtitle" 
            data={pods}
            columns={[
              {
                header: 'Name',
                field: 'metadata.name',
                renderCell: row => <Text>{row.metadata.name}</Text>
              },
              {
                header: 'Namespace',
                field: 'metadata.namespace',
                renderCell: row => <Text>{row.metadata.namespace}</Text>
              },
              {
                header: 'IP',
                field: 'status.pod_ip',
                renderCell: row => <Text>{row.status.pod_ip}</Text>
              },
            ]}
          />
        </Table.Container>
      </Box>
    </>
  );
}

export default PodsTab;

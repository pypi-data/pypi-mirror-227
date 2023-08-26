import { useState, useEffect } from 'react';
import { Box, Text } from '@primer/react';
import { Table, DataTable } from '@primer/react/drafts';
import { JupyterFrontEndProps } from '../JupyterKubernetes';
import { requestAPI } from './../handler';

type Service = {
  id: number,
  metadata: {
    name: string,
    namespace: string,
  },
}

const ServicesTab = (props: JupyterFrontEndProps) => {
  const [services, setServices] = useState(new Array<Service>());
  useEffect(() => {
    requestAPI<any>('services')
    .then(data => {
      const services = (data.services as [any]).map((service, id) => {
        return {
          id,
          ...service,
        }
      });
      setServices(services);
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
          <Table.Title as="h2" id="services">
            Services
          </Table.Title>
          <Table.Subtitle as="p" id="services-subtitle">
            List of services
          </Table.Subtitle>
          <DataTable
            aria-labelledby="services"
            aria-describedby="services-subtitle" 
            data={services}
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
            ]}
          />
        </Table.Container>
      </Box>
    </>
  );
}

export default ServicesTab;

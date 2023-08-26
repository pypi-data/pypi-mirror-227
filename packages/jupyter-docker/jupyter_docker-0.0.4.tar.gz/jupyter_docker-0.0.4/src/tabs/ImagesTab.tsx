import { useState, useEffect } from 'react';
import { Box, Text } from '@primer/react';
import { Table, DataTable } from '@primer/react/drafts';
import { requestAPI } from './../handler';
import { strip } from './../utils/Utils';

/*
Architecture: "amd64"
Author: ""
Comment: "buildkit.dockerfile.v0"
Config: {Hostname: '', Domainname: '', User: '1000', AttachStdin: false, AttachStdout: false, …}
Container: ""
ContainerConfig: {Hostname: '', Domainname: '', User: '', AttachStdin: false, AttachStdout: false, …}
Created: "2023-08-24T11:44:52.596431396Z"
DockerVersion: ""
GraphDriver: {Data: {…}, Name: 'overlay2'}
Id: "sha256:07b6ee191814172244a05eabe4ffc69f739bc162d851b2626138a563f77bea55"
Metadata: {LastTagTime: '2023-08-24T11:44:52.772168988Z'}
Os: "linux"
Parent: ""
RepoDigests: ['datalayer/jupyterpool@sha256:3202d5976cc98e5ddffa0164155f16174bca323e02396c369da11a3c8223c637']
RepoTags: ['datalayer/jupyterpool:0.0.6']
RootFS: {Type: 'layers', Layers: Array(78)}
Size: 9401017097
VirtualSize: 9401017097
*/
type DockerImage = {
  id: number,
  RepoTags: string[],
  Os: string,
  Size: number,
  Created: string,
}

const Images = () => {
  const [images, setImages] = useState(new Array<DockerImage>());
  useEffect(() => {
    requestAPI<any>('images')
    .then(data => {
      const images = (data.images as [any]).map((image, id) => {
        return {
          id,
          ...image,
        }
      }) as [DockerImage];
      setImages(images.filter(image => image.RepoTags.length > 0));
    })
    .catch(reason => {
      console.error(
        `Error while accessing the jupyter server jupyter_docker extension.\n${reason}`
      );
    });
  }, []);
  return (
    <>
      <Box>
        <Table.Container>
          <Table.Title as="h2" id="images">
            Docker images
          </Table.Title>
          <Table.Subtitle as="p" id="images-subtitle">
            List of Docker images.
          </Table.Subtitle>
          <DataTable
            aria-labelledby="images"
            aria-describedby="images-subtitle" 
            data={images}
            columns={[
              {
                header: 'RepoTags',
                field: 'RepoTags',
                renderCell: row => <>
                  { row.RepoTags.map(repoTag => <Box><Text>{strip(repoTag, 40)}</Text></Box>) 
                }</>
              },
              {
                header: 'Size',
                field: 'Size',
                renderCell: row => <Text>{row.Size}</Text>
              },
              {
                header: 'Os',
                field: 'Os',
                renderCell: row => <Text>{row.Os}</Text>
              },
            ]}
          />
        </Table.Container>
      </Box>
    </>
  )
}

export default Images;

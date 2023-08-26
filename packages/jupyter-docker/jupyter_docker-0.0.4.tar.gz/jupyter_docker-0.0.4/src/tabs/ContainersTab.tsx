import { useState, useEffect } from 'react';
import { Box, Text } from '@primer/react';
import { Table, DataTable } from '@primer/react/drafts';
import { requestAPI } from './../handler';
/*
{
  "Id": "7789a37b8945a85d4f8049d4a84b85529a9debd3701814ef8cd237cd5adb9a58",
  "Created": "2023-08-25T09:36:44.914950183Z",
  "Path": "tini",
  "Args": [
    "-g",
    "--",
    "start-jupyterpool.sh"
  ],
  "State": {
    "Status": "running",
    "Running": true,
    "Paused": false,
    "Restarting": false,
    "OOMKilled": false,
    "Dead": false,
    "Pid": 8001,
    "ExitCode": 0,
    "Error": "",
    "StartedAt": "2023-08-25T09:36:45.395331909Z",
    "FinishedAt": "0001-01-01T00:00:00Z",
    "Health": {
      "Status": "starting",
      "FailingStreak": 0,
      "Log": [
        {
          "Start": "2023-08-25T09:36:50.374146569Z",
          "End": "2023-08-25T09:36:50.599379436Z",
          "ExitCode": 1,
          "Output": "Traceback (most recent call last):\n  File \"/etc/jupyter/docker_healthcheck.py\", line 14, in <module>\n    json_file = next(runtime_dir.glob(\"*server-*.json\"))\n                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nStopIteration\n"
        }
      ]
    }
  },
  "Image": "sha256:07b6ee191814172244a05eabe4ffc69f739bc162d851b2626138a563f77bea55",
  "ResolvConfPath": "/var/lib/docker/containers/7789a37b8945a85d4f8049d4a84b85529a9debd3701814ef8cd237cd5adb9a58/resolv.conf",
  "HostnamePath": "/var/lib/docker/containers/7789a37b8945a85d4f8049d4a84b85529a9debd3701814ef8cd237cd5adb9a58/hostname",
  "HostsPath": "/var/lib/docker/containers/7789a37b8945a85d4f8049d4a84b85529a9debd3701814ef8cd237cd5adb9a58/hosts",
  "LogPath": "/var/lib/docker/containers/7789a37b8945a85d4f8049d4a84b85529a9debd3701814ef8cd237cd5adb9a58/7789a37b8945a85d4f8049d4a84b85529a9debd3701814ef8cd237cd5adb9a58-json.log",
  "Name": "/jupyterpool",
  "RestartCount": 0,
  "Driver": "overlay2",
  "Platform": "linux",
  "MountLabel": "",
  "ProcessLabel": "",
  "AppArmorProfile": "",
  "ExecIDs": null,
  "HostConfig": {
    "Binds": null,
    "ContainerIDFile": "",
    "LogConfig": {
      "Type": "json-file",
      "Config": {}
    },
    "NetworkMode": "default",
    "PortBindings": {
      "8686/tcp": [
        {
          "HostIp": "",
          "HostPort": "8686"
        }
      ]
    },
    "RestartPolicy": {
      "Name": "no",
      "MaximumRetryCount": 0
    },
    "AutoRemove": true,
    "VolumeDriver": "",
    "VolumesFrom": null,
    "ConsoleSize": [
      17,
      95
    ],
    "CapAdd": null,
    "CapDrop": null,
    "CgroupnsMode": "private",
    "Dns": [],
    "DnsOptions": [],
    "DnsSearch": [],
    "ExtraHosts": null,
    "GroupAdd": null,
    "IpcMode": "private",
    "Cgroup": "",
    "Links": null,
    "OomScoreAdj": 0,
    "PidMode": "",
    "Privileged": false,
    "PublishAllPorts": false,
    "ReadonlyRootfs": false,
    "SecurityOpt": null,
    "UTSMode": "",
    "UsernsMode": "",
    "ShmSize": 67108864,
    "Runtime": "runc",
    "Isolation": "",
    "CpuShares": 0,
    "Memory": 0,
    "NanoCpus": 0,
    "CgroupParent": "",
    "BlkioWeight": 0,
    "BlkioWeightDevice": [],
    "BlkioDeviceReadBps": [],
    "BlkioDeviceWriteBps": [],
    "BlkioDeviceReadIOps": [],
    "BlkioDeviceWriteIOps": [],
    "CpuPeriod": 0,
    "CpuQuota": 0,
    "CpuRealtimePeriod": 0,
    "CpuRealtimeRuntime": 0,
    "CpusetCpus": "",
    "CpusetMems": "",
    "Devices": [],
    "DeviceCgroupRules": null,
    "DeviceRequests": null,
    "MemoryReservation": 0,
    "MemorySwap": 0,
    "MemorySwappiness": null,
    "OomKillDisable": null,
    "PidsLimit": null,
    "Ulimits": null,
    "CpuCount": 0,
    "CpuPercent": 0,
    "IOMaximumIOps": 0,
    "IOMaximumBandwidth": 0,
    "MaskedPaths": [
      "/proc/asound",
      "/proc/acpi",
      "/proc/kcore",
      "/proc/keys",
      "/proc/latency_stats",
      "/proc/timer_list",
      "/proc/timer_stats",
      "/proc/sched_debug",
      "/proc/scsi",
      "/sys/firmware"
    ],
    "ReadonlyPaths": [
      "/proc/bus",
      "/proc/fs",
      "/proc/irq",
      "/proc/sys",
      "/proc/sysrq-trigger"
    ]
  },
  "GraphDriver": {
    "Data": {
      "LowerDir": "/var/lib/docker/overlay2/b1f7d5a4767c538865f4705591126144c59b7a1379b38a69fd4935dcb826951c-init/diff:/var/lib/docker/overlay2/z7l0tqhrxu1nceylnup68mg1r/diff:/var/lib/docker/overlay2/jpx89zlf9t4xzqol5icao2jxc/diff:/var/lib/docker/overlay2/qvyc6tgaxyhztrxbg477poj0a/diff:/var/lib/docker/overlay2/vdu8xj7yxyxbpcmm2l66cha8d/diff:/var/lib/docker/overlay2/jh9i5imiag9gj1qzd18xno1db/diff:/var/lib/docker/overlay2/otyppu5qldysedycbubbi0dvq/diff:/var/lib/docker/overlay2/xhigjrrrbx5hhvjt4pl447g2j/diff:/var/lib/docker/overlay2/qty9akl7olzsdj5mzdeda0aaf/diff:/var/lib/docker/overlay2/l2m8d344o414zl7480q264z2s/diff:/var/lib/docker/overlay2/eq2w046lu27js428ml29lxkfw/diff:/var/lib/docker/overlay2/tu71d8uxey83hbs1h78e8cnq2/diff:/var/lib/docker/overlay2/v8mepdxozz9q1oiyr380o1yhx/diff:/var/lib/docker/overlay2/nglpuo5y8qnxae57m5op1fxl7/diff:/var/lib/docker/overlay2/ocx48vw8m7f9vcgdo7no8xjn8/diff:/var/lib/docker/overlay2/ynv8lgcy12ozflywr4h1oq14s/diff:/var/lib/docker/overlay2/rwimb1rvp1x6hu9ukkw86b0i7/diff:/var/lib/docker/overlay2/oiyxtqjg3z0euf010z4bjzlri/diff:/var/lib/docker/overlay2/xu8s6yoq2o5k9rsgplusvu3dd/diff:/var/lib/docker/overlay2/33dhym10x3n4vkpug2vrc20ky/diff:/var/lib/docker/overlay2/yjkkky4xenawiwhv981h8nzla/diff:/var/lib/docker/overlay2/vjrawayms9581ijq106iivzgk/diff:/var/lib/docker/overlay2/r23s9ubao3dna8fhfnvtqw0m9/diff:/var/lib/docker/overlay2/c8udkshmnnrmjiscdxvdpmwhg/diff:/var/lib/docker/overlay2/7s8kwpecrc8eahxzcq45t8e5f/diff:/var/lib/docker/overlay2/rpt949bfdxquu0q0yae85e2es/diff:/var/lib/docker/overlay2/y26uz13g4o3k0i8y9zcsorfp8/diff:/var/lib/docker/overlay2/1zd6re9i3myy9i7hmrln7dc1p/diff:/var/lib/docker/overlay2/cqtitrz46jjma9kpibldjpo8g/diff:/var/lib/docker/overlay2/p7ggu579k3ns2skn5dw8v9owq/diff:/var/lib/docker/overlay2/v5ny229s7n8x1gxelyw25tsj3/diff:/var/lib/docker/overlay2/u9ck89wyer98m8jh447atlros/diff:/var/lib/docker/overlay2/mayhlxjc1omzdsqhj6bl3idcz/diff:/var/lib/docker/overlay2/oepa25jeod2zrh2r8rk5wlp12/diff:/var/lib/docker/overlay2/cql9z2kag919ctf6zf0hw310i/diff:/var/lib/docker/overlay2/gr4pssp3esazohk8xzwi09oip/diff:/var/lib/docker/overlay2/5172w8rteec5ry7ilhfrobt5y/diff:/var/lib/docker/overlay2/2jkek8e1pib4ilcb7kkg0xht1/diff:/var/lib/docker/overlay2/1eya4shk63elg4nx7350rk8gy/diff:/var/lib/docker/overlay2/r6o2jo30ct0fkj43cl69woauc/diff:/var/lib/docker/overlay2/i9utxk1z2v5yvlkt9r89d2c9i/diff:/var/lib/docker/overlay2/n2esz7e2qv58638k7qpi97wn5/diff:/var/lib/docker/overlay2/l8vgescrijln8fqgmyqt68nzn/diff:/var/lib/docker/overlay2/zw5c1xhppuo5e932zioraj2a0/diff:/var/lib/docker/overlay2/n5jwdn4819r8on5u7407e8oy8/diff:/var/lib/docker/overlay2/mzdf4qjjt8eiz3t7pookscy9l/diff:/var/lib/docker/overlay2/v2dyu3anqjn7g5t581nhi015o/diff:/var/lib/docker/overlay2/hxh0zdjloub8j20y4zlc9h5vn/diff:/var/lib/docker/overlay2/pxasi1umpz60zadwbwwchcnp0/diff:/var/lib/docker/overlay2/o8nw1zawnntprlliivuj3s26y/diff:/var/lib/docker/overlay2/5guy7xxek4c5n5ragvn3w7odq/diff:/var/lib/docker/overlay2/195284d3623def91e19ff8b9a0656bd5c8205d782eb2b0169bb13ab804b462ca/diff:/var/lib/docker/overlay2/8dc1fce15d97cd80663f8026800c820f0f811846a591cfc41329bc0f045090a0/diff:/var/lib/docker/overlay2/d3e51cf6ae410860899e3fad262d28fba6308f75c3a038b42748dbaf9c567afc/diff:/var/lib/docker/overlay2/7f9b34d377565513e990def7af6f0b91f3ff95a5dccc5b12c4b8e9a602cf1bb7/diff:/var/lib/docker/overlay2/658bd2e5c5d1fd62733ac2cfe6109449ecdcbd0d8450469936ebe439f9b81985/diff:/var/lib/docker/overlay2/535a55e49c4a5f7d213ade501a2da3899d1ad1e01263a5a8dee69191f9f893c3/diff:/var/lib/docker/overlay2/0059fed943ed788b8db251f05e271977beb59fbe65a109eedbef06908dc4be45/diff:/var/lib/docker/overlay2/dfd0600c900306663fa0d338e8a3cf24a7ec3c9218320db486280961afa19113/diff:/var/lib/docker/overlay2/1c77968de818cafab774a2ea7b3910e9e083196a4e3e420542d3068b6ad091d7/diff:/var/lib/docker/overlay2/b1faf84610f5faeeb963087922d37c0dc4a3c7fe013cfecc58b0887be791e7bb/diff:/var/lib/docker/overlay2/c9ab9cf6827d12d72cb9281d634e6e3504f5152afdc68f8fb843b1bc9c216e87/diff:/var/lib/docker/overlay2/3a19ce87d395c4c079d97ca8cc772b4f70b3c178831926a2f1e64fdb6d0056b2/diff:/var/lib/docker/overlay2/447d0a66f44958f53aa76e9ff025825fcc1c6c583c4828d50584303abaa4a5e6/diff:/var/lib/docker/overlay2/4245353a832a822bb6576fc548b5e813d4eaba13dcc1ecdf9d26e527aa053501/diff:/var/lib/docker/overlay2/49a019cf23acc98309b7194fde6f01586a08f9eed2cc8a199b4b4b54deb34f03/diff:/var/lib/docker/overlay2/e4d0b47455fedd1a93476adca2b2c7d89a0a1378b220b0e11434645e01b92127/diff:/var/lib/docker/overlay2/456ae03a0e8b2f4836bb0d83ffa4175ae8fafaf745b31da5c1cd6181e94cfec8/diff:/var/lib/docker/overlay2/a0b8223acdb5806c32ff3a164737aea92c807ec2fe06017e9332d41bae0b2707/diff:/var/lib/docker/overlay2/ad6d6742a26e4133cc3b4674b38ad25932c5591dfea11403761ad74b74a5a81b/diff:/var/lib/docker/overlay2/c161d71ea98918787b94c21f664d3902d18f91c8d5e4af179092b4ff3730b246/diff:/var/lib/docker/overlay2/4fb53a2b60d788f89fdafce85b05368d25b3717110332a34c83f6eeff5af2764/diff:/var/lib/docker/overlay2/b6c86e2bfd9434e0c9cdfd8c391b30bb6c5acc8933c63714eb4a1261636aa3c5/diff:/var/lib/docker/overlay2/b59bcaa94f4e6d9b346d80b05cf37d9b2f041845bc5fc460435c8384a912d338/diff:/var/lib/docker/overlay2/fa781e1a4f7128b28819eaebcd8be2147dd2967ff070a7526804598b701cbcb4/diff:/var/lib/docker/overlay2/42139830801e44d004aa580a358028f76edbafb9320416984473c8a065cffb97/diff:/var/lib/docker/overlay2/5f4194017ee9c95e164e1eaef1a568fb245ba7599c8e485c3b5c720119e6012e/diff:/var/lib/docker/overlay2/33fc950fad717d5d4594479dbeeabee404d576c06dcc49b75f286b2de75ac031/diff:/var/lib/docker/overlay2/7edd3a3ee621267f4783057483fdf39a29bb15a6fa2f4a0185327de545c647d8/diff",
      "MergedDir": "/var/lib/docker/overlay2/b1f7d5a4767c538865f4705591126144c59b7a1379b38a69fd4935dcb826951c/merged",
      "UpperDir": "/var/lib/docker/overlay2/b1f7d5a4767c538865f4705591126144c59b7a1379b38a69fd4935dcb826951c/diff",
      "WorkDir": "/var/lib/docker/overlay2/b1f7d5a4767c538865f4705591126144c59b7a1379b38a69fd4935dcb826951c/work"
    },
    "Name": "overlay2"
  },
  "Mounts": [],
  "Config": {
    "Hostname": "7789a37b8945",
    "Domainname": "",
    "User": "1000",
    "AttachStdin": true,
    "AttachStdout": true,
    "AttachStderr": true,
    "ExposedPorts": {
      "8686/tcp": {},
      "8888/tcp": {}
    },
    "Tty": true,
    "OpenStdin": true,
    "StdinOnce": true,
    "Env": [
      "GITHUB_CLIENT_ID=",
      "GITHUB_CLIENT_SECRET=",
      "GITHUB_OAUTH_CALLBACK_URL=http://localhost:8686/api/jupyterpool/login",
      "PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "DEBIAN_FRONTEND=noninteractive",
      "CONDA_DIR=/opt/conda",
      "SHELL=/bin/bash",
      "NB_USER=jovyan",
      "NB_UID=1000",
      "NB_GID=100",
      "LC_ALL=en_US.UTF-8",
      "LANG=en_US.UTF-8",
      "LANGUAGE=en_US.UTF-8",
      "HOME=/home/jovyan",
      "JUPYTER_PORT=8888",
      "XDG_CACHE_HOME=/home/jovyan/.cache/"
    ],
    "Cmd": [
      "start-jupyterpool.sh"
    ],
    "Healthcheck": {
      "Test": [
        "CMD-SHELL",
        "/etc/jupyter/docker_healthcheck.py || exit 1"
      ],
      "Interval": 5000000000,
      "Timeout": 3000000000,
      "StartPeriod": 5000000000,
      "Retries": 3
    },
    "Image": "datalayer/jupyterpool:0.0.6",
    "Volumes": null,
    "WorkingDir": "/home/jovyan",
    "Entrypoint": [
      "tini",
      "-g",
      "--"
    ],
    "OnBuild": null,
    "Labels": {
      "maintainer": "Jupyter Project <jupyter@googlegroups.com>",
      "org.opencontainers.image.ref.name": "ubuntu",
      "org.opencontainers.image.version": "22.04"
    }
  },
  "NetworkSettings": {
    "Bridge": "",
    "SandboxID": "44e0a3b65f116583aecec630f20b1a59232d1c306e913a975f4f248ebd06b9f2",
    "HairpinMode": false,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "Ports": {
      "8686/tcp": [
        {
          "HostIp": "0.0.0.0",
          "HostPort": "8686"
        }
      ],
      "8888/tcp": null
    },
    "SandboxKey": "/var/run/docker/netns/44e0a3b65f11",
    "SecondaryIPAddresses": null,
    "SecondaryIPv6Addresses": null,
    "EndpointID": "c7fb9552d1ec1f9c9cf29db31492d7ec930dfd08098271910a8e82b62e55a54b",
    "Gateway": "172.17.0.1",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "IPAddress": "172.17.0.2",
    "IPPrefixLen": 16,
    "IPv6Gateway": "",
    "MacAddress": "02:42:ac:11:00:02",
    "Networks": {
      "bridge": {
        "IPAMConfig": null,
        "Links": null,
        "Aliases": null,
        "NetworkID": "2746e97d6b90898f77dfa2278954d6b4afa68533a9eb190374b917f6c9eb7087",
        "EndpointID": "c7fb9552d1ec1f9c9cf29db31492d7ec930dfd08098271910a8e82b62e55a54b",
        "Gateway": "172.17.0.1",
        "IPAddress": "172.17.0.2",
        "IPPrefixLen": 16,
        "IPv6Gateway": "",
        "GlobalIPv6Address": "",
        "GlobalIPv6PrefixLen": 0,
        "MacAddress": "02:42:ac:11:00:02",
        "DriverOpts": null
      }
    }
  }
}
*/
type DockerContainer = {
  id: number,
  Id: string,
  Created: string,
  Config: {
    Image: string,
  }
}

const Containers = () => {
  const [containers, setContainers] = useState(new Array<DockerContainer>());
  useEffect(() => {
    requestAPI<any>('containers')
    .then(data => {
      const containers = (data.containers as [any]).map((container, id) => {
        return {
          id,
          ...container,
        }
      }) as [DockerContainer];
      setContainers(containers);
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
          <Table.Title as="h2" id="containers">
            Docker containers
          </Table.Title>
          <Table.Subtitle as="p" id="containers-subtitle">
            List of Docker containers.
          </Table.Subtitle>
          <DataTable
            aria-labelledby="containers"
            aria-describedby="containers-subtitle" 
            data={containers}
            columns={[
              {
                header: 'Image',
                field: 'Config.Image',
                renderCell: row => <Text>{row.Config.Image}</Text>
              },
              {
                header: 'Id',
                field: 'Id',
                renderCell: row => <Text>{row.Id}</Text>
              },
              {
                header: 'Created',
                field: 'Created',
                renderCell: row => <Text>{row.Created}</Text>
              },
            ]}
          />
        </Table.Container>
      </Box>
    </>
  );
}

export default Containers;

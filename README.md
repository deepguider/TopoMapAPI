# Topological Map Server & Client
### Updates V0.5
- 부천지역 추가
- Routing Layer 생성 방식 변경
    - 보차혼용로 추가: Node type - 2, Edge type - 1
    - 이상한 모양의 노드 연결 제거
    - Edge length 계산시 버그 수정    

### 다운로드 및 압축 해제
  - 이메일에 제공된 링크로부터 Topological Map server docker 이미지 파일을 다운로드 받음 (topomapserver_package.tar)
 
### Server 실행 (Topological map API와 Routing API 가 동시에 실행됨)
  - 아래의 서버 실행시 Topological Map을 구성하는 세 가지 layer를 다운로드할 수 있는 서버가 동시에 실행 됨
  
  ```bash
  tar xjf server_*.tar.bz2
  docker load -i topomapserver.tar
  docker load -i routingapi_server.tar
  docker-compose -f naver_api_docker_compose.yml up
  ```
  
### 인터페이스
1. tile 번호를 이용하는 방법: http://path.to.server/tile/tile_num_x/tile_num_y/
2. 위경도 값을 이용하는 방법: http://path.to.server/wgs/latitude/longitude/radius
3. layer의 node id를 이용하는 방법 (V0.4): http://path.to.server/node/node_id/radius
4. Routing layer의 node id를 이용하는 방법 (V0.4): http://path.to.server/routing_node/node_id/radius
- 비고: 위치별 사용가능한 tile 번호
    - 봉은사 지역: tile_num_bong.txt
    - 에트리 지역: tile_num_etri.txt
    - 부천 지역: tile_num_bucheon.txt
     
### Client 샘플 코드
1. topomap_client.py 수정
    - "localhost" 를 서버의 ip address로 변경
    - Port number는 바꾸지 말 것

2. 클라이언트 실행
    ```bash
    python topomap_client.py <layer> <request_type>
    ```
    
    - layer: routing, poi, or streetview
    - request_type: tile, wgs, or node

# Routing server & Client
### 다운로드 및 압축 해제
  - 이메일에 제공된 링크로부터 docker 이미지 파일을 다운로드 받음 (routingapi_server.tar)

### 서버 실행 (Topological map API와 Routing API 가 동시에 실행됨)
  ```bash
  docker load -i topomapserver.tar
  docker load -i routingapi_server.tar
  docker-compose -f naver_api_docker_compose.yml up
  ```
  
### 인터페이스
  - 경로 생성:
    - http://path.to.server/start_lat/start_lon/goal_lat/goal_lon/num_paths
  - Delete edge (V0.4)
    - http://path.to.server/delete/edge_num
  - Restore edge (V0.4)
    - http://path.to.server/restore/edge_num
    
### Client 샘플 코드
1. routing_client.py 수정
    - "localhost" 를 서버의 ip address로 변경
    - Port number는 바꾸지 말 것

2. 클라이언트 실행
    ```bash
    python routing_client.py 
    ```
    - 예제 1: ETRI 및 봉은사 지역 시작점->도착점
    - 예제 2: ETRI 지역 시작점->경유지->도착점

# Image download server & Client
### 다운로드 및 압축 해제
  - 이메일에 제공된 링크로부터 image server docker 이미지 파일을 다운로드 받음 (imageserver_package.tar)
  - 아래의 커맨드를 실행하여 압축 해제
  ```bash
  mkdir -p imageserver && cd imageserver
  tar xf imageserver_package.tar
  ```

### 서버 실행 
  ```bash
  cd imageserver
  docker load -i imageserver.tar
  PORT=10000 ./run.sh ~/path/to/bongeunsa_image or ~/path/to/etri_image
  ```
  
### 클라이언트 실행
  - 인터페이스
    - Panorama: http://ip.address.to.image.server:port/streetview_id
    - Cubic: ttp://ip.address.to.image.server:port/streetview_id/{face}
  - Example
    ```
    curl http://ip.address.to.image.server:port/29300503300 --output test.jpg
    ```

# Visualization
 - geojson.io 에 접속후 geojson 파일을 드래그 & 드롭
 - geojson.io 의 기본 지도가 네이버지도가 아니므로 다소 어긋나 보일 수는 있음
 - QGIS:
    - link: https://www.qgis.org/ko/site/
# 관련 문의
- 이동환: donghwan.lee@naverlabs.com
- 김덕화: deokhwa.kim@naverlabs.com

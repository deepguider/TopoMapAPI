# Topological Map Server & Client
### Updates V0.7
- ETRI 지역 Crosswalk 개선
- edge 및 node type 오류 해결
- node type 수정 (보차혼용로 노드 타입 제거)

### Updates V0.6
- ETRI 지역 실내 추가
- Routing 개선:
    - 일부 routing node, edge 업데이트 (수작업)
    - Shortest path 기준을 node 수가 아닌 이동 거리로 변경

### Updates V0.5
- 부천지역 추가
- Routing Layer 생성 방식 변경
    - 보차혼용로 추가: Node type - 2, Edge type - 1
    - 이상한 모양의 노드 연결 제거
    - Edge length 계산시 버그 수정    

## 실내 지역 Topomap 생성 규칙
### 지도/경로 체계
- 실내/실외를 별도 구분된 맵이 아닌 단일 graph 지도로 처리 (floor 속성으로 실내외 구분)
- 실내외에 걸친 path도 기존과 동일한 단일 path로 표현
- 실내/실외 모두 POI 맵은 Routing Map과는 분리된 독립된 layer로 표현

### Routing Map과 POI Map의 관계
- Routing 노드와 POI 노드들의 위치는 실내외 모두 GPS 좌표로 표현
- (기본적으로) Routing Map과 POI Map 노드들 사이의 직접적인 연결관계는 없음
- (일부 지역에 한하여) 토폴로지 노드에 연결된 POI들을 부가정보로 제공할 수 있음: Routing layer의 노드 속성 정보 중 ["properties"]["pois"] 항목
   
### Routing Layer의 node 및 edge 의 type
- Node:
    - 인도: 0
    - 분기점: 1
    - 문 앞: 2
    - 엘리베이터: 3
    - 에스컬레이터: 4
- Edge:
    - 인도: 0
    - 보차혼용로: 1
    - 횡단보도: 2
    - 엘리베이터 연결: 3
    - 에스컬레이터 연결: 4
    - 계단 연결: 5
    - 실내/실외 연결: 6
    
### 수직 이동: 
- 엘리베이터 노드는 각 엘리베이터마다 하나씩 배치됨 (층 마다 따로 두지 않음)
- 각 노드는 각 층 마다 엘리베이터 앞의 문에 배치된 노드들과 연결되어 있음
- 에트리의 경우에는 총 2개의 엘리베이터 노드가 존재하고 각 층에 있는 node들과 연결됨 
- 아래 예시에서 엘리베이터 노드는 3개의 edge를 갖음 (1F, 3F, 7F 에 연결되는)
![image](https://user-images.githubusercontent.com/51685843/124554816-55f93c00-de71-11eb-9062-dcea696a0102.png)

### 실내/실외 연결
- 출입구 (혹은 문) 노드는 type 3으로 지정됨
- Outdoor 쪽 출입구는 type 3, floor 0의 값을 갖음
- Indoor 쪽 출입구는 type 3, floor 1의 값을 갖음 (아래 예시 참고. 1층에서 연결 시)
- 두 출입구를 이어주는 edge는 type 6, floor 1의 값을 갖음
![image](https://user-images.githubusercontent.com/51685843/124554658-29ddbb00-de71-11eb-87da-ae76f63aaf9b.png)

### Routing API 변경
- Routing API 호출시 층 정보를 부가적으로 넣어주어야 함 (outdoor: 0)

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
  
### 인터페이스 (updated @ V0.6)
  - 경로 생성: floor는 층 정보 (outdoor의 경우 0) 
    - http://path.to.server/start_lat/start_lon/floor/goal_lat/goal_lon/floor/num_paths
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

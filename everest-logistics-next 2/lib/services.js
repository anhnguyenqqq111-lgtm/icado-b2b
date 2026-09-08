export const serviceGroups=[
 {name:'Vận Chuyển Quốc Tế',items:[
  {name:'Vận chuyển đường biển (FCL/LCL)',slug:'van-chuyen-duong-bien',image:'service-container.jpeg'},
  {name:'Vận chuyển hàng không khẩn cấp',slug:'van-chuyen-hang-khong',image:'everlog-banner-2.jpeg'},
  {name:'Vận chuyển Door-to-Door',slug:'door-to-door',image:'everlog-banner-3.jpeg'},
  {name:'Hàng siêu trường siêu trọng (OOG)',slug:'hang-oog',image:'service-oog.jpeg'}]},
 {name:'Hải Quan & XNK',items:[
  {name:'Khai báo hải quan trọn gói',slug:'khai-bao-hai-quan',image:'service-customs.jpeg'},
  {name:'Ủy thác Xuất Nhập Khẩu B2B',slug:'uy-thac-xuat-nhap-khau',image:'service-customs.jpeg'},
  {name:'Dịch vụ Tạm nhập – Tái xuất',slug:'tam-nhap-tai-xuat',image:'service-container.jpeg'},
  {name:'Tư vấn Mã HS & Xin C/O',slug:'ma-hs-xin-co',image:'service-customs.jpeg'}]},
 {name:'Giấy Phép Chuyên Ngành',items:[
  {name:'Xin Giấy phép nhập khẩu',slug:'giay-phep-nhap-khau',image:'service-customs.jpeg'},
  {name:'Công bố Thực phẩm & Mỹ phẩm',slug:'cong-bo-thuc-pham-my-pham',image:'everlog-banner-4.jpeg'},
  {name:'Kiểm dịch Thực vật & Động vật',slug:'kiem-dich',image:'service-customs.jpeg'},
  {name:'Chứng nhận Hợp quy & Hun trùng',slug:'hop-quy-hun-trung',image:'service-customs.jpeg'}]},
 {name:'Nội Địa & Hỗ Trợ',items:[
  {name:'Vận tải đường bộ Bắc Nam',slug:'van-tai-bac-nam',image:'everlog-banner-3.jpeg'},
  {name:'Chằng buộc & Lashing máy móc',slug:'lashing-may-moc',image:'service-lashing.png'},
  {name:'Bảo hiểm hàng hóa đường biển',slug:'bao-hiem-hang-hoa',image:'service-container.jpeg'},
  {name:'Dịch vụ Kho bãi & Đóng gói',slug:'kho-bai-dong-goi',image:'everlog-banner-4.jpeg'}]}
];
export const services=serviceGroups.flatMap(group=>group.items.map(item=>({...item,group:group.name})));
export const getService=slug=>services.find(service=>service.slug===slug);
export const partners=['partner-one.png','partner-evergreen.png','partner-cma-cgm.png','partner-cargolux.png','partner-turkish.png','partner-qatar.png','partner-msc.png','partner-cosco.png','partner-09.png','partner-sicart-smith.png','partner-phd.png','partner-kim-qui-ups.png'];

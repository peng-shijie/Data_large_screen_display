from  flask  import  Flask, json,render_template
from  flask  import  request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)

# 配置 MySQL 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/quality_reports'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 报表模型
class Report(db.Model):
    __tablename__ = 'reports'  # 数据库表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)  # 日期
    internal_defect_rate = db.Column(db.Numeric(5, 2))  # 坯不良率
    machine_material_waste_rate = db.Column(db.Numeric(5, 2))  # 机加料废率
    machining_waste_rate = db.Column(db.Numeric(5, 2))  # 机加工废率
    machine_defect_rate = db.Column(db.Numeric(5, 2))  # 毛坯不良率
    comprehensive_leakage_rate = db.Column(db.Numeric(5, 2))  # 综合泄漏率
    customer_complaints_official = db.Column(db.Integer)  # 客诉件数
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间


# 质量问题模型
class QualityIssue(db.Model):
    __tablename__ = 'quality_issues'  # 数据库表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)  # 日期
    quality_type = db.Column(db.String(50), nullable=False)  # 质量类型
    product_name = db.Column(db.String(100), nullable=False)  # 产品名称
    defect_type = db.Column(db.String(100), nullable=False)  # 不良类型
    input_qty = db.Column(db.Integer, nullable=False)  # 投入数量
    defect_qty = db.Column(db.Integer, nullable=False)  # 不良数量
    defect_rate = db.Column(db.Numeric(5, 2))  # 不良率
    problem_description = db.Column(db.Text)  # 问题描述
    remarks = db.Column(db.String(200))  # 备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间


# 客户投诉模型
class CustomerComplaint(db.Model):
    __tablename__ = 'customer_complaints'  # 数据库表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)  # 日期
    customer_name = db.Column(db.String(100))  # 客户名称
    complaint_description = db.Column(db.Text)  # 投诉问题描述
    handling_status = db.Column(db.Text)  # 处理情况
    remarks = db.Column(db.String(200))  # 备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间


@app.route('/')
def  index():
  return  render_template('index.html')


@app.route('/index-1')
def  new():
  return  render_template('index-1.html')
  
@app.route('/submit_report', methods=['POST'])
def submit_report():
    data = request.json

    try:
        # 1. 保存 Report 主表
        report = Report(
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            internal_defect_rate=Decimal(data['main_indicators']['internalDefectRate'].strip('%')),
            machine_material_waste_rate=Decimal(data['main_indicators']['machineMaterialWasteRate'].strip('%')),
            machining_waste_rate=Decimal(data['main_indicators']['machiningWasteRate'].strip('%')),
            machine_defect_rate=Decimal(data['main_indicators']['machineDefectRate'].strip('%')),
            comprehensive_leakage_rate=Decimal(data['main_indicators']['comprehensiveLeakageRate'].strip('%')),
            customer_complaints_official=int(data['main_indicators']['customerComplaintsOfficial'])
        )
        db.session.add(report)
        db.session.flush()  # 获取 report.id 用于关联（如果你需要）

        # 2. 保存 quality_issues
        for issue in data['quality_issues']:
            quality_issue = QualityIssue(
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                quality_type=issue['qualityType'],
                product_name=issue['productName'],
                defect_type=issue['defectType'],
                input_qty=int(issue['inputQty']),
                defect_qty=int(issue['defectQty']),
                defect_rate=Decimal(issue['defectRate'].strip('%')),
                problem_description=issue.get('problemDescription', ''),
                remarks=issue.get('remarks', '')
            )
            db.session.add(quality_issue)

        # 3. 保存 customer_complaints（如果有）
        for complaint in data.get('customer_complaints', []):
            customer_complaint = CustomerComplaint(
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                customer_name=complaint.get('customerName', ''),
                complaint_description=complaint.get('complaintDescription', ''),
                handling_status=complaint.get('handlingStatus', ''),
                remarks=complaint.get('remarks', '')
            )
            db.session.add(customer_complaint)

        db.session.commit()
        return jsonify({"status": "success", "message": "日报提交成功"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"提交失败: {str(e)}"}), 500



if  __name__ == '__main__':
  app.run(host='0.0.0.0',  port=5000,  debug=True)
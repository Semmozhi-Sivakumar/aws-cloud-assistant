import {
  ShieldCheck,
  AlertTriangle,
  ShieldAlert,
  CheckCircle2,
} from "lucide-react";

function Security() {
  return (
    <>
      {/* Header */}
      <header className="header">
        <div>
          <p className="eyebrow">SECURITY CENTER</p>
          <h1>Security</h1>
          <p className="subtitle">
            Review security findings detected in your AWS environment.
          </p>
        </div>
      </header>

      {/* Security Overview */}
      <section className="security-overview">
        <div className="security-score">
          <div className="score-icon">
            <ShieldCheck size={32} />
          </div>

          <div>
            <p className="eyebrow">ENVIRONMENT STATUS</p>
            <h2>Needs Attention</h2>
            <p>
              Your AWS environment has security findings that should be reviewed.
            </p>
          </div>
        </div>

        <div className="security-summary">
          <div className="summary-item critical-summary">
            <span>1</span>
            <p>Critical</p>
          </div>

          <div className="summary-item warning-summary">
            <span>1</span>
            <p>Review</p>
          </div>

          <div className="summary-item medium-summary">
            <span>1</span>
            <p>Medium</p>
          </div>
        </div>
      </section>

      {/* Findings */}
      <section className="section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">FINDINGS</p>
            <h2>Security Findings</h2>
          </div>

          <span className="finding-count">3 findings</span>
        </div>

        <div className="security-findings">

          {/* Critical Finding */}
          <div className="security-finding critical">
            <div className="security-finding-icon">
              <ShieldAlert size={22} />
            </div>

            <div className="security-finding-content">
              <div className="finding-title">
                <h3>Public S3 Access</h3>
                <span className="severity">Critical</span>
              </div>

              <p>
                The bucket policy allows public read access to objects,
                which may expose stored files to unauthorized users.
              </p>

              <div className="recommendation">
                <strong>Recommendation:</strong>
                Review the bucket policy and block unnecessary public access.
              </div>
            </div>
          </div>

          {/* Review Finding */}
          <div className="security-finding warning">
            <div className="security-finding-icon">
              <AlertTriangle size={22} />
            </div>

            <div className="security-finding-content">
              <div className="finding-title">
                <h3>Broad S3 Permissions</h3>
                <span className="severity">Review</span>
              </div>

              <p>
                The IAM user <strong>image_upload_user</strong> has
                AmazonS3FullAccess permissions.
              </p>

              <div className="recommendation">
                <strong>Recommendation:</strong>
                Follow the principle of least privilege and restrict
                permissions to only the required S3 actions.
              </div>
            </div>
          </div>

          {/* Medium Finding */}
          <div className="security-finding medium">
            <div className="security-finding-icon">
              <AlertTriangle size={22} />
            </div>

            <div className="security-finding-content">
              <div className="finding-title">
                <h3>S3 Versioning Disabled</h3>
                <span className="severity">Medium</span>
              </div>

              <p>
                Object versioning is currently disabled for the S3 bucket.
              </p>

              <div className="recommendation">
                <strong>Recommendation:</strong>
                Enable versioning to help recover previous versions of
                objects after accidental deletion or modification.
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* Positive Security Note */}
      <section className="security-positive">
        <CheckCircle2 size={22} />

        <div>
          <h3>Security monitoring is active</h3>
          <p>
            Your Cloud Assistant is continuously ready to analyze
            available AWS environment information.
          </p>
        </div>
      </section>
    </>
  );
}

export default Security;
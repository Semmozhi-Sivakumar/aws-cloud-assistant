import {
  HeartPulse,
  CheckCircle2,
  Server,
  Database,
  BellRing,
  Activity,
} from "lucide-react";

function Health() {
  return (
    <>
      {/* Header */}
      <header className="header">
        <div>
          <p className="eyebrow">ENVIRONMENT HEALTH</p>
          <h1>Health</h1>
          <p className="subtitle">
            Monitor the overall health and status of your AWS environment.
          </p>
        </div>
      </header>

      {/* Overall Health Status */}
      <section className="health-overview">
        <div className="health-status">
          <div className="health-icon">
            <HeartPulse size={34} />
          </div>

          <div>
            <p className="eyebrow">OVERALL STATUS</p>
            <h2>Environment Stable</h2>
            <p>
              No active CloudWatch alarms are currently detected in the
              monitored AWS environment.
            </p>
          </div>
        </div>

        <div className="health-badge">
          <CheckCircle2 size={20} />
          Operational
        </div>
      </section>

      {/* Service Health */}
      <section className="section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">SERVICE STATUS</p>
            <h2>AWS Service Health</h2>
          </div>

          <span className="finding-count">4 services monitored</span>
        </div>

        <div className="health-grid">

          {/* EC2 */}
          <div className="health-card">
            <div className="health-card-top">
              <div className="health-service-icon">
                <Server size={22} />
              </div>

              <span className="service-status neutral">
                No instances
              </span>
            </div>

            <h3>EC2</h3>

            <p>
              No EC2 instances are currently running in this environment.
            </p>
          </div>

          {/* S3 */}
          <div className="health-card">
            <div className="health-card-top">
              <div className="health-service-icon">
                <Database size={22} />
              </div>

              <span className="service-status healthy">
                Healthy
              </span>
            </div>

            <h3>S3 Storage</h3>

            <p>
              1 S3 bucket is accessible and available for monitoring.
            </p>
          </div>

          {/* CloudWatch */}
          <div className="health-card">
            <div className="health-card-top">
              <div className="health-service-icon">
                <BellRing size={22} />
              </div>

              <span className="service-status healthy">
                No alarms
              </span>
            </div>

            <h3>CloudWatch</h3>

            <p>
              No active CloudWatch alarms are currently detected.
            </p>
          </div>

          {/* Monitoring */}
          <div className="health-card">
            <div className="health-card-top">
              <div className="health-service-icon">
                <Activity size={22} />
              </div>

              <span className="service-status healthy">
                Active
              </span>
            </div>

            <h3>Monitoring</h3>

            <p>
              AWS environment information is available for analysis.
            </p>
          </div>

        </div>
      </section>

      {/* Health Note */}
      <section className="health-note">
        <CheckCircle2 size={22} />

        <div>
          <h3>Monitoring status is normal</h3>
          <p>
            No immediate operational issues were detected from the currently
            available AWS environment data.
          </p>
        </div>
      </section>
    </>
  );
}

export default Health;
import { type NuxtAxiosInstance } from "@nuxtjs/axios";
import { BackendJob } from "../types/dataset";

class JobStatus {
  constructor(public readonly jobId: string, private readonly status: string) {}

  get isQueued() {
    return this.status === "queued";
  }

  get isFinished() {
    return this.status === "finished";
  }

  get isFailed() {
    return this.status === "failed";
  }

  get isStarted() {
    return this.status === "started";
  }

  get isDeferred() {
    return this.status === "deferred";
  }

  get isScheduled() {
    return this.status === "scheduled";
  }

  get isStopped() {
    return this.status === "stopped";
  }

  get isCanceled() {
    return this.status === "canceled";
  }

  get isRunning() {
    return (
      this.isStarted || this.isScheduled || this.isQueued || this.isDeferred
    );
  }
}

export class JobRepository {
  constructor(private readonly axios: NuxtAxiosInstance) {}

  async getJobStatus(jobId: string): Promise<JobStatus> {
    try {
      const { data } = await this.axios.get<BackendJob>(`/v1/jobs/${jobId}`);

      return new JobStatus(data.id, data.status);
    } catch {
      return new JobStatus(jobId, "failed");
    }
  }
}
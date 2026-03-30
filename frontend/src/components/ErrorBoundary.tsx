import React, { Component } from "react";
import type { ErrorInfo, ReactNode } from "react";
import { COLORS, FONTS, BUTTON_SECONDARY } from "../theme";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error("[ErrorBoundary]", error.message, errorInfo.componentStack);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div style={{
          padding: 32,
          textAlign: "center",
          color: COLORS.textMuted,
          fontFamily: FONTS.mono,
          fontSize: 11,
        }}>
          <div style={{ marginBottom: 12 }}>Something went wrong rendering this section.</div>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            style={BUTTON_SECONDARY}
          >
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

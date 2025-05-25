import '@testing-library/jest-dom';

declare global {
  namespace jest {
    type Mock<T = any, Y extends any[] = any> = {
      mockClear: () => void;
      mockReset: () => void;
      mockRestore: () => void;
      mockImplementation: (fn: (...args: Y) => T) => Mock<T, Y>;
      mockImplementationOnce: (fn: (...args: Y) => T) => Mock<T, Y>;
      mockReturnThis: () => Mock<T, Y>;
      mockReturnValue: (value: T) => Mock<T, Y>;
      mockReturnValueOnce: (value: T) => Mock<T, Y>;
      mockResolvedValue: (value: T) => Mock<T, Y>;
      mockResolvedValueOnce: (value: T) => Mock<T, Y>;
      mockRejectedValue: (value: any) => Mock<T, Y>;
      mockRejectedValueOnce: (value: any) => Mock<T, Y>;
    };
  }
}

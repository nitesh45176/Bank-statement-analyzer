import React from 'react';
import { UploadCloud, FileSpreadsheet, Activity, Database, CheckCircle, Search } from 'lucide-react';

const CashoraHeader = ({ onUploadClick, onExportClick, isConnected }) => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo & Branding */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 to-violet-700 text-white shadow-md">
            <Activity className="w-6 h-6" strokeWidth={2.5} />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-tight text-gray-900 leading-none">
                Cashora
              </h1>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800">
                v2.0
              </span>
            </div>
            <p className="text-xs text-gray-500 font-medium mt-0.5">Financial Intelligence Platform</p>
          </div>
        </div>

        {/* Global Search (Placeholder for future) */}
        <div className="hidden md:flex flex-1 max-w-md mx-8 relative">
           <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
             <Search className="h-4 w-4 text-gray-400" />
           </div>
           <input
             type="text"
             className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-gray-50 placeholder-gray-400 focus:outline-none focus:bg-white focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors duration-200"
             placeholder="Search transactions, insights, or ask AI..."
           />
        </div>

        {/* Actions & Status */}
        <div className="flex items-center space-x-4">
          
          {/* Status Indicator */}
          <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600 bg-gray-50 px-3 py-1.5 rounded-full border border-gray-200">
            {isConnected ? (
              <>
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span className="font-medium text-emerald-700">API Connected</span>
              </>
            ) : (
              <>
                <Database className="w-4 h-4 text-rose-500" />
                <span className="font-medium text-rose-700">API Disconnected</span>
              </>
            )}
          </div>

          <button
            onClick={onExportClick}
            className="hidden sm:inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
          >
            <FileSpreadsheet className="w-4 h-4 mr-2 text-green-600" />
            Export Excel
          </button>
          
          <button
            onClick={onUploadClick}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
          >
            <UploadCloud className="w-4 h-4 mr-2" />
            New Statement
          </button>
        </div>
      </div>
    </header>
  );
};

export default CashoraHeader;

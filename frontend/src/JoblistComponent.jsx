import React from 'react';

const JobList = ({ jobs }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Job Results</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {jobs.map((job, index) => (
          <div 
            key={index} 
            className="bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
          >
            <h3 className="font-bold text-lg mb-2">{job.title}</h3>
            <p className="text-gray-600 mb-1">Company: {job.company}</p>
            <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
              Keyword: {job.keyword}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JobList;